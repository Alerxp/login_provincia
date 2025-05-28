from django.db import models
from django.contrib.auth.models import User

class CUEUsuario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cues')
    cue = models.CharField("CUE", max_length=7)  # Ej: 7000001
    anexo = models.CharField("Anexo", max_length=2, blank=True, null=True)  # Ej: 00
    modalidad = models.CharField("Modalidad", max_length=3, blank=True, null=True)  # Ej: 200
    nivel = models.CharField("Nivel", max_length=3, blank=True, null=True)  # Ej: 110

    def formato_completo(self):
        partes = [self.cue]
        if self.anexo:
            partes.append(self.anexo)
        if self.modalidad:
            partes.append(self.modalidad)
        if self.nivel:
            partes.append(self.nivel)
        return "-".join(partes)
