from django.contrib import admin
from .models import DadosImportados

class DadosImportadosAdmin(admin.ModelAdmin):
    # Campos exibidos na lista de registros
    list_display = (
        'ref_giant',
        'mawb',
        'hawb',
        'q',
        'sostatus_releasedonholdreturned',
        'data_liberacao',
        'numero_nfe',
        'status_impexp',
        'dlvatdestination'
    )
    
    # Campos editáveis diretamente na lista
    list_editable = (
        'q',
        'sostatus_releasedonholdreturned',
        'data_liberacao',
        'numero_nfe',
        'status_impexp',
        'dlvatdestination'
    )
    
    # Filtros laterais
    list_filter = (
        'q',
        'sostatus_releasedonholdreturned',
        'status_impexp',
        'data_liberacao',
        'data_nfe',
    )
    
    # Campos de busca
    search_fields = (
        'ref_giant',
        'mawb',
        'hawb',
        'numero_nfe',
        'nftg',
        'diduenumber',
    )
    
    # Campos agrupados no formulário de edição
    fieldsets = (
        ('Identificação', {
            'fields': ('ref_giant', 'mawb', 'hawb')
        }),
        ('Status Operacional', {
            'fields': (
                'q',
                'sostatus_releasedonholdreturned',
                'data_liberacao',
                'status_impexp'
            )
        }),
        ('Documentos Fiscais', {
            'fields': (
                'data_nfe',
                'numero_nfe',
                'nftgdt',
                'nftg'
            )
        }),
        ('Entrega', {
            'fields': ('dlvatdestination',)
        }),
        ('Eventos', {
            'fields': ('eventos',),
            'classes': ('wide',)
        }),
        ('Outras Informações', {
            'classes': ('collapse',),
            'fields': (
                'cipbrl',
                'peso',
                'li',
                'diduenumber'
            )
        })
    )
    
    # Texto vazio para campos não preenchidos
    empty_value_display = '-N/D-'
    
    # Itens por página
    list_per_page = 25
    
    # Ordenação padrão
    ordering = ('-data_liberacao',)
    
    # Atalhos para datas
    date_hierarchy = 'data_liberacao'
    
    # Mostra links de salvamento no topo também
    save_on_top = True

admin.site.register(DadosImportados, DadosImportadosAdmin)
