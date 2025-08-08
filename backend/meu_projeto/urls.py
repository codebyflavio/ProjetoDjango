from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rota unificada da API
    path('api/', include('api.urls')),
    path('api/', include('dados_importados.urls')),  # isso deve existir

    # Autenticação (login/logout)
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
