from django.contrib import admin
from .models import DesembaracoAduaneiro

@admin.register(DesembaracoAduaneiro)
class DesembaracoAduaneiroAdmin(admin.ModelAdmin):
    list_display = [
        'referencia_giant', 'mawb', 'codigos', 'status_liberacao', 'data_liberacao',
        'valor', 'peso', 'data_emissao', 'data_prevista_entrega', 'eventos',
        'dias_atraso', 'tipo_justificativa_atraso', 'justificativa_atraso', 'canal_cor',
        'data_chegada_destino', 'data_ci_ok', 'data_di', 'data_ead', 'data_entrega_destino',
        'data_estimada', 'data_hawb', 'data_li', 'data_liberacao_ccr', 'data_nfe',
        'data_nfe_deloitte', 'hawb', 'icms_pago', 'li', 'numero_di', 'numero_nfe',
        'numero_nfe_deloitte', 'ok_to_ship', 'pc', 'peso_cobravel', 'status_import_export', 'status_li'
    ]
    search_fields = ['referencia_giant', 'mawb', 'codigos']
    list_filter = ['status_liberacao', 'status_import_export', 'status_li']
    ordering = ['-data_liberacao']

