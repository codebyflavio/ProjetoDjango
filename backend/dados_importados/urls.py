# dados_importados/urls.py - Define as rotas/endpoints da app dados_importados

from django.urls import path
from .views import example_api

urlpatterns = [
    path('example/', example_api, name='example_api'),
]
