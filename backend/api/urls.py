from django.urls import path
from django.http import JsonResponse
from .views import example_api, desembaraco_list

def api_root(request):
    return JsonResponse({
        "example": "/api/example/",
        "desembaraco": "/api/desembaraco/"
    })

urlpatterns = [
    path('', api_root, name='api-root'),  # rota para /api/
    path('example/', example_api, name='example-api'),
    path('desembaraco/', desembaraco_list, name='desembaraco-list'),
]
