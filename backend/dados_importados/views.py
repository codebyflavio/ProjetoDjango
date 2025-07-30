from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DadosImportados
from .serializers import DadosImportadosSerializer

@api_view(['GET'])
def desembaraco_list(request):
    dados = DadosImportados.objects.all()
    serializer = DadosImportadosSerializer(dados, many=True)
    return Response(serializer.data)
