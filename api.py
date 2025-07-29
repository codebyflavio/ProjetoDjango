
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def example_api(request):
    data = {
        'mensagem': 'Olá do Django API',
        'status': 'sucesso'
    }
    return Response(data)