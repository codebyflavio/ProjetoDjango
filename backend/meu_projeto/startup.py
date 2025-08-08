from django.contrib.auth.models import Group

def criar_grupos_padrao():
    Group.objects.get_or_create(name='editor_visualizador')
    Group.objects.get_or_create(name='visualizador')
