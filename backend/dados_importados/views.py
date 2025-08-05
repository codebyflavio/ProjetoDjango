from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import DadosImportados
from .serializers import DadosImportadosSerializer
from django.http import HttpResponse
import csv

# Lista todos os registros (com filtros/paginação) ou exporta CSV
@api_view(['GET'])
def listar_dados(request):
    queryset = DadosImportados.objects.all()
    
    # --- Filtros ---
    ref_giant = request.query_params.get('ref_giant')
    if ref_giant:
        queryset = queryset.filter(ref_giant__icontains=ref_giant)

    status_param = request.query_params.get('status')
    if status_param:
        queryset = queryset.filter(sostatus_releasedonholdreturned__iexact=status_param)

    data_inicio = request.query_params.get('data_inicio')
    data_fim = request.query_params.get('data_fim')
    if data_inicio:
        queryset = queryset.filter(data_liberacao__gte=data_inicio)
    if data_fim:
        queryset = queryset.filter(data_liberacao__lte=data_fim)

    busca = request.query_params.get('search')
    if busca:
        queryset = queryset.filter(
            Q(ref_giant__icontains=busca) |
            Q(mawb__icontains=busca) |
            Q(hawb__icontains=busca) |
            Q(deliveryid__icontains=busca)
        )

    ordenacao = request.query_params.get('ordering', '-data_liberacao')
    queryset = queryset.order_by(ordenacao)

    if request.query_params.get('format') == 'csv':
        return exportar_csv(queryset)

    pagina = int(request.query_params.get('page', 1))
    itens_por_pagina = int(request.query_params.get('page_size', 10))
    inicio = (pagina - 1) * itens_por_pagina
    fim = inicio + itens_por_pagina

    serializer = DadosImportadosSerializer(queryset[inicio:fim], many=True)

    return Response({
        'total': queryset.count(),
        'pagina': pagina,
        'itens_por_pagina': itens_por_pagina,
        'resultados': serializer.data
    })

# Detalhes de um registro específico
@api_view(['GET'])
def detalhes_dado(request, ref_giant):
    registro = get_object_or_404(DadosImportados, ref_giant=ref_giant)
    serializer = DadosImportadosSerializer(registro)
    return Response(serializer.data)

# Atualização (PUT/PATCH) de um registro
@api_view(['PUT', 'PATCH'])
def update_dado(request, ref_giant):
    dado = get_object_or_404(DadosImportados, ref_giant=ref_giant)
    serializer = DadosImportadosSerializer(dado, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Exportação CSV
def exportar_csv(queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dados_importados.csv"'

    writer = csv.writer(response, delimiter=';')
    cabecalho = [field.verbose_name for field in DadosImportados._meta.fields]
    writer.writerow(cabecalho)

    for obj in queryset:
        linha = [getattr(obj, field.name) for field in DadosImportados._meta.fields]
        writer.writerow(linha)

    return response
