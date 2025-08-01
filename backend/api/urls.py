from django.contrib import admin
from django.urls import path, include
from .views import desembaraco_list


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('dados_importados.urls')),  # Importante!
    path('desembaraco/', desembaraco_list),
]