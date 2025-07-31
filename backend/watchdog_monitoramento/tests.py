import os
import sys
import django

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meu_projeto.settings')
django.setup()

from dados_importados.models import DadosImportados
from watch_xml import process_xml_content

def print_status(title, ins, upd, unch):
    print(f"{title} → Inseridos: {ins}, Atualizados: {upd}, Sem alteração: {unch}")

def run_tests():
    
    DadosImportados.objects.all().delete()
    print("🔁 Banco limpo\n")

    
    xml_1 = """
    <Root>
        <NewReportItem><REF.GIANT>1</REF.GIANT><MAWB>agua</MAWB><HAWB>carro</HAWB></NewReportItem>
        <NewReportItem><REF.GIANT>2</REF.GIANT><MAWB>agua</MAWB><HAWB>carro</HAWB></NewReportItem>
        <NewReportItem><REF.GIANT>2</REF.GIANT><MAWB>fogo</MAWB><HAWB>barco</HAWB></NewReportItem>
        <NewReportItem><REF.GIANT>1</REF.GIANT><MAWB>fogo</MAWB><HAWB>barco</HAWB></NewReportItem>
    </Root>
    """
    ins, upd, unch = process_xml_content(xml_1)
    print_status("1) Duplicatas internas (mesmo XML)", ins, upd, unch)
    

    
    xml_2 = """
    <Root>
        <NewReportItem><REF.GIANT>1</REF.GIANT><MAWB>agua</MAWB><HAWB>moto</HAWB></NewReportItem> <!-- mudou HAWB -->
        <NewReportItem><REF.GIANT>1</REF.GIANT><MAWB>agua</MAWB><HAWB>moto</HAWB></NewReportItem> <!-- duplicata idêntica -->
        <NewReportItem><REF.GIANT>2</REF.GIANT><MAWB>fogo</MAWB><HAWB>barco</HAWB></NewReportItem> <!-- igual -->
        <NewReportItem><REF.GIANT>3</REF.GIANT><MAWB>terra</MAWB><HAWB>avião</HAWB></NewReportItem> <!-- novo -->
        <NewReportItem><REF.GIANT>3</REF.GIANT><MAWB>terra</MAWB><HAWB>avião</HAWB></NewReportItem> <!-- duplicata novo -->
    </Root>
    """
    ins, upd, unch = process_xml_content(xml_2)
    print_status("2) Duplicatas externas com atualizações", ins, upd, unch)
    

    
    xml_3 = """
    <Root>
        <NewReportItem><REF.GIANT>1</REF.GIANT><MAWB>agua</MAWB><HAWB>moto</HAWB></NewReportItem>
        <NewReportItem><REF.GIANT>2</REF.GIANT><MAWB>fogo</MAWB><HAWB>barco</HAWB></NewReportItem>
        <NewReportItem><REF.GIANT>3</REF.GIANT><MAWB>terra</MAWB><HAWB>avião</HAWB></NewReportItem>
    </Root>
    """
    ins, upd, unch = process_xml_content(xml_3)
    print_status("3) Sem alteração (dados iguais)", ins, upd, unch)
    

    total = DadosImportados.objects.count()
    print(f"\n✅ Total final no banco após testes: {total} registros (esperado: 3)")

if __name__ == "__main__":
    run_tests()
