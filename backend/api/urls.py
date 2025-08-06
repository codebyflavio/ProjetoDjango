from django.urls import path, include
from .views import user_info

urlpatterns = [
    # Rota da view que retorna o usuário autenticado
    path('user-info/', user_info),

    # Rota para os dados importados
    path('dados/', include('dados_importados.urls')),  # acessível em /api/dados/
]
