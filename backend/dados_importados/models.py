from django.db import models

class DadosImportados(models.Model):
    ref_giant = models.CharField(max_length=255, primary_key=True, verbose_name="Referência Giant")  # REF.GIANT
    mawb = models.CharField(max_length=255, blank=True, null=True, verbose_name="MAWB")
    hawb = models.CharField(max_length=255, blank=True, null=True, verbose_name="HAWB")
    q = models.CharField(max_length=255, blank=True, null=True, verbose_name="Q")
    c3 = models.CharField(max_length=255, blank=True, null=True, verbose_name="C3")
    deliveryid = models.CharField(max_length=255, blank=True, null=True, verbose_name="Delivery ID")
    sostatus_releasedonholdreturned = models.CharField(max_length=255, blank=True, null=True, verbose_name="Status RELEASED / ON HOLD / RETURNED")
    data_liberacao = models.DateField(blank=True, null=True, verbose_name="Data Liberação")  # RELEASEDDT
    cipbrl = models.CharField(max_length=255, blank=True, null=True, verbose_name="CIPBRL")
    pc = models.CharField(max_length=255, blank=True, null=True, verbose_name="PC")
    peso = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Peso")  # GROSSWEIGHT
    peso_cobravel = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Peso Cobrável")  # CHARGEABLEWEIGHT
    tipo = models.CharField(max_length=255, blank=True, null=True, verbose_name="Tipo")  # TYPE
    pupdt = models.DateField(blank=True, null=True, verbose_name="Data PUPDT")
    ciok = models.DateField(blank=True, null=True, verbose_name="Data CIOK")
    lientrydt = models.DateField(blank=True, null=True, verbose_name="Data LI Entry")
    liok = models.DateField(blank=True, null=True, verbose_name="Data LI OK")
    ok_to_ship = models.CharField(max_length=255, blank=True, null=True, verbose_name="OK to Ship")  # OKTOSHIP
    li = models.CharField(max_length=255, blank=True, null=True, verbose_name="LI")
    hawbdt = models.DateField(blank=True, null=True, verbose_name="Data HAWB")
    estimatedbookingdt = models.DateField(blank=True, null=True, verbose_name="Data Estimada Booking")
    arrivaldestinationdt = models.DateField(blank=True, null=True, verbose_name="Data Chegada Destino")
    solicitacao_fundos = models.CharField(max_length=255, blank=True, null=True, verbose_name="Solicitação de Fundos")  # FUNDSREQUEST
    fundos_recebidos = models.CharField(max_length=255, blank=True, null=True, verbose_name="Fundos Recebidos")  # FundsReceived
    eadidt = models.DateField(blank=True, null=True, verbose_name="Data EAD")
    diduedt = models.DateField(blank=True, null=True, verbose_name="Data DI Due")
    diduenumber = models.CharField(max_length=255, blank=True, null=True, verbose_name="Número DU")  # DIDUENUMBER
    icmspago = models.DateField(max_length=255, blank=True, null=True, verbose_name="ICMS Pago")  # ICMSPAID
    canal_cor = models.CharField(max_length=255, blank=True, null=True, verbose_name="Canal Cor")  # CHANNELCOLOR
    data_liberacao_ccr = models.DateField(blank=True, null=True, verbose_name="Data Liberação CCR")  # CCRLSDDT
    data_nfe = models.DateField(blank=True, null=True, verbose_name="Data NFE")  # NFEDT
    numero_nfe = models.CharField(max_length=255, blank=True, null=True, verbose_name="Número NFE")  # NFE
    nftgdt = models.CharField(max_length=255, blank=True, null=True, verbose_name="NFTGDT")
    nftg = models.CharField(max_length=255, blank=True, null=True, verbose_name="NFTG")
    dlvatdestination = models.DateField(blank=True, null=True, verbose_name="Data Chegada Destino")  # DLVATDESTINATION
    status_impexp = models.CharField(max_length=255, blank=True, null=True, verbose_name="Status Import/Export")  # StatusIMPEXP
    data_estimada = models.DateField(blank=True, null=True, verbose_name="Data Estimada")  # ESTIMATEDDATE
    eventos = models.TextField(blank=True, null=True, verbose_name="Eventos")  # EVENT (pode ser muito longo)
    real_lead_time = models.CharField(max_length=255, blank=True, null=True, verbose_name="Real Lead Time")
    ship_failure_days = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ship Failure Days")
    tipo_justificativa_atraso = models.CharField(max_length=255, blank=True, null=True, verbose_name="Tipo Justificativa Atraso")  # TYPE (duplicado no XML)
    justificativa_atraso = models.CharField(max_length=500, blank=True, null=True, verbose_name="Justificativa Atraso")  # FAILUREJUSTIFICATION

    class Meta:
        db_table = 'dados_importados'

    def __str__(self):
        return self.ref_giant
