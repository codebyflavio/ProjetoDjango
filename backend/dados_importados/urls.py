from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_dados),                    # GET /api/dados/
    path('<str:ref_giant>/', views.detalhes_dado),   # GET /api/dados/<ref_giant>/
    path('<str:ref_giant>/update/', views.update_dado),  # PUT/PATCH /api/dados/<ref_giant>/update/
]
