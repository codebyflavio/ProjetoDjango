from django.urls import path
from django.shortcuts import redirect
from .views import listar_dados

urlpatterns = [
    path('', lambda request: redirect('dados-listagem')),  # redireciona /api-backend/ para /api-backend/dados/
    path('dados/', listar_dados, name='dados-listagem'),
]
