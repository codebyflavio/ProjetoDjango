from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from dados_importados.models import DadosImportados
from dados_importados.serializers import DadosImportadosSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import Group

@login_required
def user_info(request):
    user = request.user
    grupo = user.groups.first().name if user.groups.exists() else "visualizador"
    return JsonResponse({
        "username": user.username,
        "tipo": grupo
    })


def pagina_inicial(request):
    return render(request, 'index.html')


@api_view(['GET'])
def desembaraco_list(request):
    dados = DadosImportados.objects.all()
    serializer = DadosImportadosSerializer(dados, many=True)
    return Response(serializer.data)
