import pandas as pd
import re

# Caminho para o seu CSV
caminho_arquivo = '4b17fe03-68e5-4ef0-b18e-a27acd19cbac.csv'

# Lê o CSV
df = pd.read_csv(caminho_arquivo)

# Regex para os dois formatos de data
padrao_data_1 = re.compile(r'^\d{4}-\d{2}-\d{2}$')  # YYYY-MM-DD
padrao_data_2 = re.compile(r'^\d{2}-\d{2}-\d{4}$')  # DD-MM-YYYY

colunas_com_data = []

# Verifica coluna por coluna
for coluna in df.columns:
    valores = df[coluna].astype(str).dropna()
    for valor in valores:
        if padrao_data_1.match(valor) or padrao_data_2.match(valor):
            colunas_com_data.append(coluna)
            break  # já achou pelo menos um valor com data
            

print("Colunas com valores no formato de data:")
for col in colunas_com_data:
    print(f"- {col}")
