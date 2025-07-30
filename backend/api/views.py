from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from dados_importados.models import DadosImportados
from dados_importados.serializers import DadosImportadosSerializer

def example_api(request):
    dados = [
        {"id": 1, "nome": "Produto A"},
        {"id": 2, "nome": "Produto B"},
        {"id": 3, "nome": "Produto C"}
    ]
    return JsonResponse(dados, safe=False)

@api_view(['GET'])
def desembaraco_list(request):
    dados = DadosImportados.objects.all()
    serializer = DadosImportadosSerializer(dados, many=True)
    return Response(serializer.data)
