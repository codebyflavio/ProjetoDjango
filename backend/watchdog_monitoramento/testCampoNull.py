import django
import os
import sys

# Configurar ambiente Django (ajuste o caminho conforme seu projeto)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meu_projeto.settings')
django.setup()

from dados_importados.models import DadosImportados
from django.db.models import Q

def campos_100_por_cento_nulos():
    total = DadosImportados.objects.count()
    if total == 0:
        print("Não há registros na tabela.")
        return
    
    campos = [field.name for field in DadosImportados._meta.get_fields() if hasattr(field, 'column')]

    campos_todos_nulos = []

    for campo in campos:
        count_nao_nulo = DadosImportados.objects.filter(~Q(**{f"{campo}__isnull": True})).count()
        if count_nao_nulo == 0:
            campos_todos_nulos.append(campo)

    if campos_todos_nulos:
        print("Campos 100% NULL (sem nenhum valor preenchido):")
        for c in campos_todos_nulos:
            print(f"- {c}")
    else:
        print("Nenhum campo está 100% NULL.")

if __name__ == "__main__":
    campos_100_por_cento_nulos()
