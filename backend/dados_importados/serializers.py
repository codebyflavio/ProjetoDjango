from rest_framework import serializers
from dados_importados.models import DadosImportados

class DadosImportadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = DadosImportados
        fields = '__all__'  # Todos os campos do modelo