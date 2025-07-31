import xml.etree.ElementTree as ET

def extrair_ref_giant(xml_content):
    root = ET.fromstring(xml_content)
    items = root.findall('.//NewReportItem')
    ref_giants = set()

    for item in items:
        ref_elem = item.find('REF.GIANT')
        if ref_elem is not None:
            valor = (ref_elem.text or '').strip()
            if valor:
                ref_giants.add(valor)

    return ref_giants

def comparar_xmls(caminho_xml1, caminho_xml2):
    with open(caminho_xml1, encoding='utf-8') as f1, open(caminho_xml2, encoding='utf-8') as f2:
        conteudo1 = f1.read()
        conteudo2 = f2.read()

    ref_giants1 = extrair_ref_giant(conteudo1)
    ref_giants2 = extrair_ref_giant(conteudo2)

    count1 = len(ref_giants1)
    count2 = len(ref_giants2)

    print(f"Quantidade de ref_giant no arquivo 1 ({caminho_xml1}): {count1}")
    print(f"Quantidade de ref_giant no arquivo 2 ({caminho_xml2}): {count2}")

    if count1 == count2:
        print("Os dois arquivos têm a mesma quantidade de ref_giant.")
        return

    maior = max(count1, count2)
    menor = min(count1, count2)
    diferenca = maior - menor
    percentual = (diferenca / menor) * 100 if menor != 0 else float('inf')

    print(f"O maior tem {maior} ref_giant, que é {diferenca} a mais que o menor.")
    print(f"Isto representa um aumento de {percentual:.2f}% em relação ao menor.")

if __name__ == "__main__":
    # Altere os caminhos para os seus arquivos XML
    arquivo_xml_1 = r'C:\Projetos\ProjetoDjango\1642 linhas Dia 24.XML'
    arquivo_xml_2 = r'C:\Projetos\ProjetoDjango\1389 linhas Dia 21.XML'

    comparar_xmls(arquivo_xml_1, arquivo_xml_2)
