from django.urls import path, include
from .views import user_info

urlpatterns = [
    # Rota para os dados importados
    path('dados/', include('dados_importados.urls')),  # acessível em /api/dados/
]
