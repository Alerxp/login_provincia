from django.db import models
from django.contrib.auth.models import User

class CUEUsuario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cues')
    cue = models.CharField(max_length=12)

    def __str__(self):
        return f"{self.user.username} - {self.cue}"
