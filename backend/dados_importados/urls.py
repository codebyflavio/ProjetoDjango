# dados_importados/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_dados),  # GET /api/dados/
    path('dados/<str:referencia_giant>/', views.DadosDetailView.as_view(), name='dados_detail'),  # nova
    
]
