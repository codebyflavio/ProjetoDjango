import os
import sys
import time
import logging
import django
import xml.etree.ElementTree as ET
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from django.db import transaction
from datetime import datetime
import hashlib

def setup_django():
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meu_projeto.settings')
    django.setup()

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
    return logging.getLogger(__name__)

MONITORED_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'pastaMonitorada'))
MAX_RETRIES = 5

FIELD_MAP = {
    'Q': 'ref_quarter',
    'C3': 'ge_celma',
    'DELIVERYID': 'codigos',
    'SOSTATUS-RELEASEDONHOLDRETURNED': 'status_liberacao',
    'MAWB': 'mawb',
    'HAWB': 'hawb',
    'CIPBRL': 'valor',
    'GROSSWEIGHT': 'peso',
    'CHARGEABLEWEIGHT': 'peso_cobravel',
    'PUPDT': 'data_emissao',
    'CIOK': 'data_ci_ok',
    'ESTIMATEDBOOKINGDT': 'data_prevista_entrega',
    'ARRIVALDESTINATIONDT': 'data_chegada_destino',
    'REF.GIANT': 'referencia_giant',
    'DIDUENUMBER': 'numero_di',
    'DIDUEDT': 'data_di',
    'ICMSPAID': 'icms_pago',
    'CHANNELCOLOR': 'canal_cor',
    'CCRLSDDT': 'data_liberacao_ccr',
    'NFEDT': 'data_nfe',
    'NFE': 'numero_nfe',
    'NFTGDT': 'data_nfe_deloitte',
    'NFTG': 'numero_nfe_deloitte',
    'DLVATDESTINATION': 'data_entrega_destino',
    'StatusIMPEXP': 'status_import_export',
    'ESTIMATEDDATE': 'data_estimada',
    'EVENT': 'eventos',
    'SHIPFAILUREDAYS': 'dias_atraso',
    'TYPE': 'tipo_justificativa_atraso',
    'FAILUREJUSTIFICATION': 'justificativa_atraso',
    'LIOK': 'status_li',
    'OKTOSHIP': 'ok_to_ship',
    'LI': 'li',
    'LIENTRYDT': 'data_li',
    'HAWBDT': 'data_hawb',
    'EADIDT': 'data_ead',
    'PC': 'pc',
}

class XMLFileHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.file_hashes = {}
        self.success_count = 0
        self.error_count = 0

    def _calculate_file_hash(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                return hashlib.md5(file.read()).hexdigest()
        except Exception as error:
            logger.warning(f"Falha ao calcular hash de {file_path}: {error}")
            return None

    def _log_file_change(self, action, file_path):
        current_hash = self._calculate_file_hash(file_path)
        if current_hash != self.file_hashes.get(file_path):
            logger.info(f"[{action}] {os.path.basename(file_path)} | Hash: {current_hash}")
            self.file_hashes[file_path] = current_hash
            return True
        return False

    def _parse_xml(self, file_path):
        for attempt in range(MAX_RETRIES):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    return ET.parse(file).getroot()
            except Exception as error:
                logger.warning(f"Tentativa {attempt + 1}: Falha ao ler {file_path} - {error}")
                time.sleep(1)
        return None

    def _process_xml_item(self, xml_item):
        item_data = {}
        for xml_tag, model_field in FIELD_MAP.items():
            raw_value = xml_item.findtext(xml_tag, '').strip() or None
            item_data[model_field] = raw_value

        if not item_data.get('codigos'):
            item_data['codigos'] = f"SEM-CODIGO-{int(time.time())}"

        try:
            with transaction.atomic():
                DesembaracoAduaneiro.objects.update_or_create(
                    codigos=item_data['codigos'],
                    defaults=item_data
                )
            self.success_count += 1
        except Exception as error:
            logger.error(f"Erro ao salvar item: {error}", exc_info=True)
            self.error_count += 1

    def _update_counters(self, total_items):
        print(f"\rProcessados: {total_items} | Sucessos: {self.success_count} | Erros: {self.error_count}", end='', flush=True)

    def _process_xml_file(self, file_path):
        xml_root = self._parse_xml(file_path)
        if not xml_root:
            self.error_count += 1
            return

        items = xml_root.findall('NewReportItem')
        for xml_item in items:
            self._process_xml_item(xml_item)

        self._update_counters(len(items))

    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith('.xml'):
            if self._log_file_change("CRIADO", event.src_path):
                self._process_xml_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory and event.src_path.lower().endswith('.xml'):
            if self._log_file_change("MODIFICADO", event.src_path):
                self._process_xml_file(event.src_path)

if __name__ == '__main__':
    logger = setup_logging()
    setup_django()
    from dados_importados.models import DesembaracoAduaneiro

    os.makedirs(MONITORED_DIR, exist_ok=True)
    logger.info(f"Monitorando: {MONITORED_DIR}")

    observer = Observer()
    handler = XMLFileHandler()
    observer.schedule(handler, path=MONITORED_DIR, recursive=False)
    observer.start()
    logger.info("Monitoramento ativo. Pressione Ctrl+C para parar.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Encerrando...")
        logger.info(f"Resumo final: {handler.success_count} sucesso(s), {handler.error_count} erro(s).")
        observer.stop()
    observer.join()
