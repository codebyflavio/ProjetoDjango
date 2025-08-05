from django.db import models

class DadosImportados(models.Model):
    # Choices para campos pré-definidos
    STATUS_CHOICES = [
        ('RELEASED', 'Released'),
        ('ON_HOLD', 'On Hold'),
        ('RETURNED', 'Returned'),
    ]
    
    Q_CHOICES = [
        ('Q1', 'Q1'),
        ('Q2', 'Q2'),
        ('Q3', 'Q3'),
        ('Q4', 'Q4'),
    ]
    
    STATUS_IMPEXP_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('LIBERADO', 'Liberado'),
        ('BLOQUEADO', 'Bloqueado'),
        ('CANCELADO', 'Cancelado'),
    ]

    # ===== CAMPOS NÃO EDITÁVEIS (dados originais) =====
    ref_giant = models.CharField(max_length=255, primary_key=True, verbose_name="Referência Giant")  
    mawb = models.CharField(max_length=255, blank=True, null=True, verbose_name="MAWB")
    hawb = models.CharField(max_length=255, blank=True, null=True, verbose_name="HAWB")
    c3 = models.CharField(max_length=255, blank=True, null=True, verbose_name="C3")
    deliveryid = models.CharField(max_length=255, blank=True, null=True, verbose_name="Delivery ID")
    cipbrl = models.CharField(max_length=255, blank=True, null=True, verbose_name="CIPBRL")
    pc = models.CharField(max_length=255, blank=True, null=True, verbose_name="PC")
    peso = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Peso")  
    peso_cobravel = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Peso Cobrável")  
    tipo = models.CharField(max_length=255, blank=True, null=True, verbose_name="Tipo")  
    pupdt = models.DateField(blank=True, null=True, verbose_name="Data PUPDT")
    ciok = models.DateField(blank=True, null=True, verbose_name="Data CIOK")
    lientrydt = models.DateField(blank=True, null=True, verbose_name="Data LI Entry")
    liok = models.DateField(blank=True, null=True, verbose_name="Data LI OK")
    ok_to_ship = models.CharField(max_length=255, blank=True, null=True, verbose_name="OK to Ship")  
    li = models.CharField(max_length=255, blank=True, null=True, verbose_name="LI")
    hawbdt = models.DateField(blank=True, null=True, verbose_name="Data HAWB")
    estimatedbookingdt = models.DateField(blank=True, null=True, verbose_name="Data Estimada Booking")
    arrivaldestinationdt = models.DateField(blank=True, null=True, verbose_name="Data Chegada Destino")
    solicitacao_fundos = models.CharField(max_length=255, blank=True, null=True, verbose_name="Solicitação de Fundos")  
    fundos_recebidos = models.CharField(max_length=255, blank=True, null=True, verbose_name="Fundos Recebidos")  
    eadidt = models.DateField(blank=True, null=True, verbose_name="Data EAD")
    diduedt = models.DateField(blank=True, null=True, verbose_name="Data DI Due")
    diduenumber = models.CharField(max_length=255, blank=True, null=True, verbose_name="Número DU")  
    icmspago = models.DateField(blank=True, null=True, verbose_name="ICMS Pago")  
    canal_cor = models.CharField(max_length=255, blank=True, null=True, verbose_name="Canal Cor")  
    data_liberacao_ccr = models.DateField(blank=True, null=True, verbose_name="Data Liberação CCR")  
    data_estimada = models.DateField(blank=True, null=True, verbose_name="Data Estimada")  
    real_lead_time = models.CharField(max_length=255, blank=True, null=True, verbose_name="Real Lead Time")
    ship_failure_days = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ship Failure Days")
    tipo_justificativa_atraso = models.CharField(max_length=255, blank=True, null=True, verbose_name="Tipo Justificativa Atraso")  
    justificativa_atraso = models.CharField(max_length=500, blank=True, null=True, verbose_name="Justificativa Atraso")

    # ===== CAMPOS EDITÁVEIS PELO USUÁRIO =====
    q = models.CharField(
        max_length=2,
        choices=Q_CHOICES,
        blank=True,
        null=True,
        verbose_name="Quarter (Q)"
    )
    
    sostatus_releasedonholdreturned = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        blank=True,
        null=True,
        verbose_name="Status Operacional"
    )
    
    data_liberacao = models.DateField(
        blank=True,
        null=True,
        verbose_name="Data de Liberação"
    )
    
    data_nfe = models.DateField(
        blank=True,
        null=True,
        verbose_name="Data da NFE"
    )
    
    numero_nfe = models.CharField(
        max_length=55,
        blank=True,
        null=True,
        verbose_name="Número da NFE"
    )
    
    nftgdt = models.DateField(
        blank=True,
        null=True,
        verbose_name="Data da NFTG"
    )
    
    nftg = models.CharField(
        max_length=55,
        blank=True,
        null=True,
        verbose_name="Número da NFTG"
    )
    
    dlvatdestination = models.DateField(
        blank=True,
        null=True,
        verbose_name="Entrega no Destino"
    )
    
    status_impexp = models.CharField(
        max_length=20,
        choices=STATUS_IMPEXP_CHOICES,
        blank=True,
        null=True,
        verbose_name="Status Importação/Exportação"
    )
    
    eventos = models.TextField(
        blank=True,
        null=True,
        verbose_name="Histórico de Eventos"
    )

    class Meta:
        db_table = 'dados_importados'
        verbose_name = 'Documento Importado'
        verbose_name_plural = 'Documentos Importados'
        ordering = ['-data_liberacao']

    def __str__(self):
        return f"{self.ref_giant} - {self.get_sostatus_releasedonholdreturned_display() or 'Sem status'}"