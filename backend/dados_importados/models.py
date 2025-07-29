from django.db import models

class DesembaracoAduaneiro(models.Model):
    referencia_giant = models.CharField(max_length=255, null=False, blank=False)
    mawb = models.CharField(max_length=255, null=False, blank=False)
    codigos = models.CharField(max_length=255, blank=True, null=True)
    status_liberacao = models.CharField(max_length=255, blank=True, null=True)
    data_liberacao = models.CharField(max_length=255, blank=True, null=True)
    valor = models.CharField(max_length=255, blank=True, null=True)
    peso = models.CharField(max_length=255, blank=True, null=True)
    data_emissao = models.CharField(max_length=255, blank=True, null=True)
    data_prevista_entrega = models.CharField(max_length=255, blank=True, null=True)
    eventos = models.TextField(blank=True, null=True)
    dias_atraso = models.CharField(max_length=255, blank=True, null=True)
    tipo_justificativa_atraso = models.CharField(max_length=255, blank=True, null=True)
    justificativa_atraso = models.CharField(max_length=255, blank=True, null=True)
    canal_cor = models.CharField(max_length=255, blank=True, null=True)
    data_chegada_destino = models.CharField(max_length=255, blank=True, null=True)
    data_ci_ok = models.CharField(max_length=255, blank=True, null=True)
    data_di = models.CharField(max_length=255, blank=True, null=True)
    data_ead = models.CharField(max_length=255, blank=True, null=True)
    data_entrega_destino = models.CharField(max_length=255, blank=True, null=True)
    data_estimada = models.CharField(max_length=255, blank=True, null=True)
    data_hawb = models.CharField(max_length=255, blank=True, null=True)
    data_li = models.CharField(max_length=255, blank=True, null=True)
    data_liberacao_ccr = models.CharField(max_length=255, blank=True, null=True)
    data_nfe = models.CharField(max_length=255, blank=True, null=True)
    data_nfe_deloitte = models.CharField(max_length=255, blank=True, null=True)
    hawb = models.CharField(max_length=255, blank=True, null=True)
    icms_pago = models.CharField(max_length=255, blank=True, null=True)
    li = models.CharField(max_length=255, blank=True, null=True)
    numero_di = models.CharField(max_length=255, blank=True, null=True)
    numero_nfe = models.CharField(max_length=255, blank=True, null=True)
    numero_nfe_deloitte = models.CharField(max_length=255, blank=True, null=True)
    ok_to_ship = models.CharField(max_length=255, blank=True, null=True)
    pc = models.CharField(max_length=255, blank=True, null=True)
    peso_cobravel = models.CharField(max_length=255, blank=True, null=True)
    status_import_export = models.CharField(max_length=255, blank=True, null=True)
    status_li = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['referencia_giant', 'mawb'], name='unique_refgiant_mawb'),
        ]

    def __str__(self):
        return f"{self.referencia_giant} - {self.mawb}"
