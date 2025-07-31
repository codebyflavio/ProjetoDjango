import os
import time
import shutil
from datetime import datetime, date
from decimal import Decimal
import xml.etree.ElementTree as ET
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import django
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meu_projeto.settings')
django.setup()

from dados_importados.models import DadosImportados
from django.db.models import DateField, DecimalField


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
    def normaliza(valor):
        if valor is None or valor == "":
            return None
        if isinstance(valor, str):
            s = valor.strip().lower()
            if s in ("none", "null", ""):
                return None
            try:
                if "." in s or "," in s:
                    return float(s.replace(",", "."))
                return int(s)
            except Exception:
                return s
        if isinstance(valor, Decimal):
            return float(valor)
        if isinstance(valor, (datetime, date)):
            return valor.strftime("%Y-%m-%d")
        return valor

    for k, v_xml in data.items():
        v_banco = getattr(obj, k, None)
        if normaliza(v_banco) != normaliza(v_xml):
            return False
    return True

def process_xml_content(xml_content: str) -> tuple[int, int, int]:
    try:
        root = ET.fromstring(xml_content)
        items = root.findall('.//NewReportItem')
        log_info(f"Processando XML com {len(items)} itens encontrados")
        
        tag_to_field = {
            'REF.GIANT': 'ref_giant',
            'MAWB': 'mawb',
            'HAWB': 'hawb',
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

            for field in DadosImportados._meta.get_fields():
                if not hasattr(field, 'column'):
                    continue
                name = field.name
                raw = data.get(name)
                if isinstance(field, DateField) and isinstance(raw, str):
                    data[name] = parse_date(raw)
                elif isinstance(field, DecimalField) and isinstance(raw, str):
                    try:
                        data[name] = Decimal(raw.replace(',', '.'))
                    except Exception:
                        data[name] = None

            if not data.get('ref_giant'):
                log_warning(f"Item sem REF.GIANT encontrado, ignorando")
                continue

            try:
                obj = DadosImportados.objects.get(ref_giant=data['ref_giant'])
            except DadosImportados.DoesNotExist:
                obj = None

            if obj is None:
                DadosImportados.objects.create(**data)
                inserted += 1
                log_success(f"Novo item inserido - REF.GIANT: {data['ref_giant']}")
            else:
                if dados_sao_iguais(obj, data):
                    unchanged += 1
                    log_info(f"Item sem alterações - REF.GIANT: {data['ref_giant']}")
                else:
                    for k, v in data.items():
                        setattr(obj, k, v)
                    obj.save()
                    updated += 1
                    log_success(f"Item atualizado - REF.GIANT: {data['ref_giant']}")

        return inserted, updated, unchanged
        
    except Exception as e:
        log_error(f"Erro ao processar XML: {str(e)}")
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
                time.sleep(2)  
                
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
                log_error(f"Falha no processamento do arquivo {filename}: {e}")
            
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