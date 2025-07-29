from django.urls import path
from .views import exemplo_api

urlpatterns = [
    path('exemplo/', exemplo_api),
]
