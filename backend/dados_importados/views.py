from django.http import HttpResponse

def index(request):
    return HttpResponse("Sistema rodando! Página inicial.")
