from rest_framework import serializers
from .models import DadosImportados

class DadosImportadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = DadosImportados
        fields = '__all__'
