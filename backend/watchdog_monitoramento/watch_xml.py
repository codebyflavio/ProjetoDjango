import os
import time
import shutil
from datetime import datetime, date
from decimal import Decimal, InvalidOperation
import xml.etree.ElementTree as ET
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import django
import sys

# Setup Django
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meu_projeto.settings')
django.setup()

from dados_importados.models import DadosImportados
from django.db.models import DateField, DecimalField

# Configuração de cores para os logs
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

BASE_DIR = os.path.dirname(__file__)
PASTA_MONITORADA = os.path.join(BASE_DIR, 'pastaMonitorada')
PASTA_LIDOS = os.path.join(BASE_DIR, 'pastaLidos')
os.makedirs(PASTA_MONITORADA, exist_ok=True)
os.makedirs(PASTA_LIDOS, exist_ok=True)

def log_info(message):
    print(f"{Colors.BLUE}[INFO]{Colors.END} {message}")

def log_success(message):
    print(f"{Colors.GREEN}[SUCCESS]{Colors.END} {message}")

def log_warning(message):
    print(f"{Colors.YELLOW}[WARNING]{Colors.END} {message}")

def log_error(message):
    print(f"{Colors.RED}[ERROR]{Colors.END} {message}")

def limpar_ref_giant(valor: str) -> str:
    if not valor:
        return ''
    return valor.replace(' ', '').replace('.', '').replace('-', '').strip()

def parse_date(date_str):
    if not date_str:
        return None
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str.strip(), fmt).date()
        except ValueError:
            continue
    return None

def dados_sao_iguais(obj, data):
    def normaliza_valor(valor, field):
        if valor is None or valor == "":
            return None
        
        # Para campos Decimal
        if isinstance(field, DecimalField):
            try:
                if isinstance(valor, str):
                    return Decimal(valor.replace(',', '.'))
                if isinstance(valor, (Decimal, float, int)):
                    return Decimal(str(valor))
            except (InvalidOperation, ValueError):
                return None
        
        # Para campos Date
        if isinstance(field, DateField):
            if isinstance(valor, str):
                return parse_date(valor)
            if isinstance(valor, (date, datetime)):
                return valor.date() if isinstance(valor, datetime) else valor
        
        # Para outros campos
        return str(valor).strip().lower() if valor else None

    for field in DadosImportados._meta.get_fields():
        if not hasattr(field, 'column') or field.name not in data:
            continue
            
        valor_xml = normaliza_valor(data[field.name], field)
        valor_banco = normaliza_valor(getattr(obj, field.name), field)
        
        if valor_xml != valor_banco:
            log_info(f"Diferença encontrada no campo {field.name}: "
                    f"Banco='{valor_banco}' vs XML='{valor_xml}'")
            return False
            
    return True

def process_xml_content(xml_content: str) -> tuple[int, int, int]:
    try:
        root = ET.fromstring(xml_content)
        items = root.findall('.//NewReportItem')
        
        if not items:
            log_warning("XML não contém nenhum item NewReportItem")
            return 0, 0, 0
            
        log_info(f"Processando XML com {len(items)} itens encontrados")
        
        tag_to_field = {
            'Q': 'q',
            'C3': 'c3',
            'DELIVERYID': 'deliveryid',
            'SOSTATUS-RELEASEDONHOLDRETURNED': 'sostatus_releasedonholdreturned',
            'RELEASEDDT': 'data_liberacao',
            'MAWB': 'mawb',
            'HAWB': 'hawb',
            'CIPBRL': 'cipbrl',
            'REF.GIANT': 'ref_giant',
            'PC': 'pc',
            'GROSSWEIGHT': 'peso',
            'CHARGEABLEWEIGHT': 'peso_cobravel',
            'TYPE': 'tipo',
            'PUPDT': 'pupdt',
            'CIOK': 'ciok',
            'LIENTRYDT': 'lientrydt',
            'LIOK': 'liok',
            'OKTOSHIP': 'ok_to_ship',
            'LI': 'li',
            'HAWBDT': 'hawbdt',
            'ESTIMATEDBOOKINGDT': 'estimatedbookingdt',
            'ARRIVALDESTINATIONDT': 'arrivaldestinationdt',
            'FUNDSREQUEST': 'solicitacao_fundos',
            'FundsReceived': 'fundos_recebidos',
            'EADIDT': 'eadidt',
            'DIDUEDT': 'diduedt',
            'DIDUENUMBER': 'diduenumber',
            'ICMSPAID': 'icmspago',
            'CHANNELCOLOR': 'canal_cor',
            'CCRLSDDT': 'data_liberacao_ccr',
            'NFEDT': 'data_nfe',
            'NFE': 'numero_nfe',
            'NFTGDT': 'nftgdt',
            'NFTG': 'nftg',
            'DLVATDESTINATION': 'dlvatdestination',
            'StatusIMPEXP': 'status_impexp',
            'ESTIMATEDDATE': 'data_estimada',
            'EVENT': 'eventos',
            'REALLEADTIME': 'real_lead_time',
            'SHIPFAILUREDAYS': 'ship_failure_days',
            'FAILUREJUSTIFICATION': 'justificativa_atraso'
        }

        inserted = 0
        updated = 0
        unchanged = 0

        for item in items:
            data = {}
            for tag_xml, field_name in tag_to_field.items():
                elem = item.find(tag_xml)
                if elem is not None and elem.text:
                    if field_name == 'ref_giant':
                        data[field_name] = limpar_ref_giant(elem.text)
                    else:
                        data[field_name] = elem.text.strip()

            # Conversão de tipos
            for field in DadosImportados._meta.get_fields():
                if not hasattr(field, 'column') or field.name not in data:
                    continue
                    
                raw = data[field.name]
                if isinstance(field, DateField) and isinstance(raw, str):
                    data[field.name] = parse_date(raw)
                elif isinstance(field, DecimalField) and isinstance(raw, str):
                    try:
                        data[field.name] = Decimal(raw.replace(',', '.'))
                    except (InvalidOperation, ValueError):
                        data[field.name] = None

            if not data.get('ref_giant'):
                log_warning("Item sem REF.GIANT encontrado, ignorando")
                continue

            try:
                obj = DadosImportados.objects.get(ref_giant=data['ref_giant'])
            except DadosImportados.DoesNotExist:
                DadosImportados.objects.create(**data)
                inserted += 1
                log_success(f"Novo item inserido - REF.GIANT: {data['ref_giant']}")
                continue

            if dados_sao_iguais(obj, data):
                unchanged += 1
                log_info(f"Item sem alterações - REF.GIANT: {data['ref_giant']}")
            else:
                log_info(f"Diferenças detectadas para REF.GIANT: {data['ref_giant']}")
                for k, v in data.items():
                    setattr(obj, k, v)
                obj.save()
                updated += 1
                log_success(f"Item atualizado - REF.GIANT: {data['ref_giant']}")

        return inserted, updated, unchanged
        
    except ET.ParseError as e:
        log_error(f"Erro ao parsear XML: {str(e)}")
        return 0, 0, 0
    except Exception as e:
        log_error(f"Erro inesperado ao processar XML: {str(e)}")
        return 0, 0, 0

class XMLHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.arquivos_lidos_com_sucesso = 0
        self.arquivos_com_erro = 0
        self.itens_inseridos = 0
        self.itens_atualizados = 0
        self.itens_sem_alteracao = 0

    def print_status(self):
        status_msg = (
            f"{Colors.BOLD}Status:{Colors.END} "
            f"Arquivos: {Colors.GREEN}✓{self.arquivos_lidos_com_sucesso}{Colors.END} | "
            f"{Colors.RED}✗{self.arquivos_com_erro}{Colors.END} | "
            f"Itens: {Colors.GREEN}+{self.itens_inseridos}{Colors.END} | "
            f"{Colors.BLUE}↗{self.itens_atualizados}{Colors.END} | "
            f"→{self.itens_sem_alteracao}"
        )
        print(status_msg.ljust(120), end='\r', flush=True)

    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith('.xml'):
            filename = os.path.basename(event.src_path)
            try:
                log_info(f"Novo arquivo detectado: {filename}")
                time.sleep(2)  # Espera para garantir escrita completa
                
                with open(event.src_path, encoding="utf-8") as f:
                    xml_content = f.read()
                
                ins, upd, unch = process_xml_content(xml_content)
                self.itens_inseridos += ins
                self.itens_atualizados += upd
                self.itens_sem_alteracao += unch
                self.arquivos_lidos_com_sucesso += 1
                
                shutil.move(event.src_path, os.path.join(PASTA_LIDOS, filename))
                log_success(f"Arquivo processado com sucesso: {filename}")
                
            except Exception as e:
                self.arquivos_com_erro += 1
                log_error(f"Falha no processamento do arquivo {filename}: {str(e)}")
            
            self.print_status()

def main():
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}SISTEMA DE MONITORAMENTO DE ARQUIVOS XML{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}[CONFIG]{Colors.END} Pasta monitorada: {os.path.abspath(PASTA_MONITORADA)}")
    print(f"{Colors.BLUE}[CONFIG]{Colors.END} Pasta de destino: {os.path.abspath(PASTA_LIDOS)}")
    print(f"{Colors.GREEN}[STATUS]{Colors.END} Iniciando monitoramento...")

    event_handler = XMLHandler()
    observer = Observer()
    observer.schedule(event_handler, PASTA_MONITORADA, recursive=False)
    observer.start()
    
    print(f"{Colors.GREEN}[STATUS]{Colors.END} Monitoramento ativo (Pressione Ctrl+C para encerrar)")
    print("-"*60)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[STATUS]{Colors.END} Encerrando monitoramento...")
        observer.stop()
    observer.join()

    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}RESUMO FINAL{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.GREEN}✓ Arquivos processados com sucesso:{Colors.END} {event_handler.arquivos_lidos_com_sucesso}")
    print(f"{Colors.RED}✗ Arquivos com erro:{Colors.END} {event_handler.arquivos_com_erro}")
    print(f"{Colors.GREEN}+ Itens inseridos:{Colors.END} {event_handler.itens_inseridos}")
    print(f"{Colors.BLUE}↗ Itens atualizados:{Colors.END} {event_handler.itens_atualizados}")
    print(f"→ Itens sem alteração: {event_handler.itens_sem_alteracao}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.GREEN}[STATUS]{Colors.END} Monitoramento encerrado")

if __name__ == "__main__":
    main()