# dados_importados/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_dados),  # GET /api/dados/
    
]
