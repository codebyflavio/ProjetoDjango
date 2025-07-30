from django.contrib import admin
from .models import DadosImportados

@admin.register(DadosImportados)
class DadosImportadosAdmin(admin.ModelAdmin):
    list_display = [
        'ref_giant', 'mawb', 'hawb', 'q', 'c3', 'deliveryid', 'sostatus_releasedonholdreturned',
        'data_liberacao', 'cipbrl', 'pc', 'peso', 'peso_cobravel', 'tipo', 'pupdt', 'ciok',
        'lientrydt', 'liok', 'ok_to_ship', 'li', 'hawbdt', 'estimatedbookingdt', 'arrivaldestinationdt',
        'solicitacao_fundos', 'fundos_recebidos', 'eadidt', 'diduedt', 'diduenumber', 'icmspago',
        'canal_cor', 'data_liberacao_ccr', 'data_nfe', 'numero_nfe', 'nftgdt', 'nftg', 'dlvatdestination',
        'status_impexp', 'data_estimada', 'eventos', 'real_lead_time', 'ship_failure_days',
        'tipo_justificativa_atraso', 'justificativa_atraso'
    ]

    search_fields = ['ref_giant', 'mawb', 'hawb', 'deliveryid']

    list_filter = [
        'sostatus_releasedonholdreturned',
        'status_impexp',
        'tipo_justificativa_atraso'
    ]

    ordering = ['-data_liberacao']
