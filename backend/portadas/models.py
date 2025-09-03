# Importaciones
from django.db import models

# Create your models here.
class Portada(models.Model):
    seccion = models.CharField(max_length = 100, null = False)
    foto = models.CharField(max_length = 100, null = True)

    def __str__(self):
        return self.seccion
    
    class Meta:
        db_table = 'portadas'
        verbose_name = 'Portada'
        verbose_name_plural = 'Portadas'