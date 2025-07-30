import os
import time
import shutil
from datetime import datetime
from decimal import Decimal
import xml.etree.ElementTree as ET
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import django
import sys

# Configurações Django
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meu_projeto.settings')
django.setup()

from dados_importados.models import DadosImportados
from django.db.models import DateField, DecimalField
from django.forms.models import model_to_dict

# Pastas
BASE_DIR = os.path.dirname(__file__)
PASTA_MONITORADA = os.path.join(BASE_DIR, 'pastaMonitorada')
PASTA_LIDOS = os.path.join(BASE_DIR, 'pastaLidos')
os.makedirs(PASTA_MONITORADA, exist_ok=True)
os.makedirs(PASTA_LIDOS, exist_ok=True)


def parse_date(date_str):
    if not date_str:
        return None
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str.strip(), fmt).date()
        except ValueError:
            continue
    return None


class XMLHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.arquivos_lidos_com_sucesso = 0
        self.arquivos_com_erro = 0
        self.itens_inseridos = 0
        self.itens_atualizados = 0
        self.itens_sem_alteracao = 0

    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith('.xml'):
            print(f"[DETECTADO] Novo arquivo XML: {event.src_path}")
            try:
                self.process_file(event.src_path)
                self.arquivos_lidos_com_sucesso += 1
            except Exception as e:
                print(f"[ERRO] Falha no processamento do arquivo {event.src_path}: {e}")
                self.arquivos_com_erro += 1

    def process_file(self, path):
        print(f"[INICIANDO PROCESSAMENTO] Arquivo: {path}")
        time.sleep(2)  # Aguarda o arquivo estabilizar

        if not os.path.exists(path):
            print(f"[ERRO] Arquivo não encontrado após espera: {path}")
            raise FileNotFoundError(f"Arquivo {path} não existe")

        try:
            tree = ET.parse(path)
            root = tree.getroot()
        except ET.ParseError as e:
            print(f"[ERRO XML] Arquivo inválido: {path} - {e}")
            raise

        items = root.findall('.//NewReportItem')
        if not items:
            print(f"[AVISO] Nenhum <NewReportItem> encontrado no arquivo {path}")
            return

        tag_to_field = {
            'REF.GIANT': 'ref_giant',
            'MAWB': 'mawb',
            'HAWB': 'hawb',
            'Q': 'q',
            'C3': 'c3',
            'DELIVERYID': 'deliveryid',
            'SOSTATUS-RELEASEDONHOLDRETURNED': 'sostatus_releasedonholdreturned',
            'RELEASEDDT': 'data_liberacao',
            'CIPBRL': 'cipbrl',
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
            'FAILUREJUSTIFICATION': 'justificativa_atraso',
        }

        for item in items:
            data = {}

            for tag_xml, field_name in tag_to_field.items():
                elem = item.find(tag_xml)
                if elem is not None and elem.text:
                    data[field_name] = elem.text.strip()

            # Conversão de tipos
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
                print("[IGNORADO] Item sem REF.GIANT.")
                continue

            # Verifica se já existe o objeto no banco
            obj = None
            try:
                obj = DadosImportados.objects.get(ref_giant=data['ref_giant'])
            except DadosImportados.DoesNotExist:
                pass

            def normalize(v):
                if isinstance(v, datetime):
                    return v.date()
                if v is None:
                    return ''
                return str(v).strip()

            if obj is None:
                DadosImportados.objects.create(**data)
                self.itens_inseridos += 1
                print(f"[NOVO] {data['ref_giant']}")
            else:
                obj_dict = model_to_dict(obj)
                obj_dict_filtered = {k: v for k, v in obj_dict.items() if k in data}

                dados_iguais = all(normalize(obj_dict_filtered.get(k)) == normalize(v) for k, v in data.items())

                if dados_iguais:
                    self.itens_sem_alteracao += 1
                    print(f"[SEM ALTERAÇÃO] {data['ref_giant']}")
                else:
                    for k, v in data.items():
                        setattr(obj, k, v)
                    obj.save()
                    self.itens_atualizados += 1
                    print(f"[ATUALIZADO] {data['ref_giant']}")

        # Move o arquivo para pastaLidos
        destino = os.path.join(PASTA_LIDOS, os.path.basename(path))
        shutil.move(path, destino)
        print(f"[ARQUIVO MOVIDO] {destino}")


def main():
    print("[SISTEMA] Iniciando monitoramento...")
    print(f"[CONFIG] Pasta monitorada: {os.path.abspath(PASTA_MONITORADA)}")
    print(f"[CONFIG] Pasta de destino: {os.path.abspath(PASTA_LIDOS)}")

    event_handler = XMLHandler()
    observer = Observer()
    observer.schedule(event_handler, PASTA_MONITORADA, recursive=False)
    observer.start()
    print("[SISTEMA] Monitoramento ativo")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[SISTEMA] Encerrando monitoramento...")
        observer.stop()
    observer.join()

    # Exibe resumo final
    print("\n[RESUMO FINAL]")
    print(f"Arquivos lidos com sucesso: {event_handler.arquivos_lidos_com_sucesso}")
    print(f"Arquivos com erro: {event_handler.arquivos_com_erro}")
    print(f"Itens inseridos: {event_handler.itens_inseridos}")
    print(f"Itens atualizados: {event_handler.itens_atualizados}")
    print(f"Itens sem alteração: {event_handler.itens_sem_alteracao}")

    print("[SISTEMA] Monitoramento encerrado")


if __name__ == "__main__":
    main()
