# dados_importados/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_dados),  # GET /api/dados/
    path('<str:ref_giant>/', views.detalhes_ou_update_dado),  # GET, PUT, PATCH /api/dados/<ref_giant>/
]
