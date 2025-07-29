from django.http import JsonResponse

def exemplo_api(request):
    data = {"mensagem": "API funcionando!"}
    return JsonResponse(data)
