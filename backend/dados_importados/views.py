from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import DadosImportados
from .serializers import DadosImportadosSerializer
from rest_framework.generics import RetrieveUpdateAPIView

# 🔎 Filtros reutilizáveis para listagem
def aplicar_filtros(queryset, params):
    if ref := params.get('ref_giant'):
        queryset = queryset.filter(ref_giant__icontains=ref)

    if status_param := params.get('status'):
        queryset = queryset.filter(sostatus_releasedonholdreturned__iexact=status_param)

    if data_inicio := params.get('data_inicio'):
        queryset = queryset.filter(data_liberacao__gte=data_inicio)

    if data_fim := params.get('data_fim'):
        queryset = queryset.filter(data_liberacao__lte=data_fim)

    if busca := params.get('search'):
        queryset = queryset.filter(
            Q(ref_giant__icontains=busca) |
            Q(mawb__icontains=busca) |
            Q(hawb__icontains=busca) |
            Q(deliveryid__icontains=busca)
        )

    return queryset


# 📄 Paginação simples (sem usar DRF pagination)
def paginar_queryset(queryset, pagina, itens_por_pagina):
    inicio = (pagina - 1) * itens_por_pagina
    fim = inicio + itens_por_pagina
    return queryset[inicio:fim]


# 🔁 Listagem de dados com filtros, ordenação, paginação e CSV opcional
@api_view(['GET'])
def listar_dados(request):
    queryset = DadosImportados.objects.all()
    queryset = aplicar_filtros(queryset, request.query_params)

    ordenacao = request.query_params.get('ordering', '-data_liberacao')
    queryset = queryset.order_by(ordenacao)


    # Paginação simples
    pagina = int(request.query_params.get('page', 1))
    itens_por_pagina = int(request.query_params.get('page_size', 10))
    dados_paginados = paginar_queryset(queryset, pagina, itens_por_pagina)

    serializer = DadosImportadosSerializer(dados_paginados, many=True)

    return Response({
        'total': queryset.count(),
        'pagina': pagina,
        'itens_por_pagina': itens_por_pagina,
        'resultados': serializer.data
    })


# 🔁 GET, PUT e PATCH em uma única view
@api_view(['GET', 'PUT', 'PATCH'])
def detalhes_ou_update_dado(request, ref_giant):
    dado = get_object_or_404(DadosImportados, ref_giant=ref_giant)

    if request.method == 'GET':
        serializer = DadosImportadosSerializer(dado)
        return Response(serializer.data)

    # PUT ou PATCH
    partial = request.method == 'PATCH'
    serializer = DadosImportadosSerializer(dado, data=request.data, partial=partial)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    print("ERROS DE VALIDAÇÃO:", serializer.errors)  # <-- Adicione isso
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DadosDetailView(RetrieveUpdateAPIView):
    queryset = DadosImportados.objects.all()
    serializer_class = DadosImportadosSerializer

    # campo no modelo que identifica o registro
    lookup_field = 'ref_giant'           # <-- nome do campo real no modelo
    # nome do parâmetro na URL que está sendo usado no requests
    lookup_url_kwarg = 'referencia_giant'  # <-- mantém a sua URL atual