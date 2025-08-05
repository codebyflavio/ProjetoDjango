from django.urls import path
from django.shortcuts import redirect
from .views import listar_dados, update_dado, detalhes_dado

urlpatterns = [
    path('', lambda request: redirect('dados-listagem')),
    path('dados/', listar_dados, name='dados-listagem'),
    path('dados/<str:ref_giant>/', update_dado, name='dados-update'),
    path('dados/<str:ref_giant>/detalhes/', detalhes_dado, name='dados-detalhes'),
]
