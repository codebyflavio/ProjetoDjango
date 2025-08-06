from django.contrib import admin
from .views import user_info
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-backend/', include('dados_importados.urls')),
    path('user-info/', user_info),
]
