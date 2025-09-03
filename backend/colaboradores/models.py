# Importaciones
from django.db import models

# Create your models here.
class Colaborador(models.Model):
    nombre = models.CharField(max_length = 100, null = False)
    foto = models.CharField(max_length = 100, null = True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'colaboradores'
        verbose_name = 'Colaborador'
        verbose_name_plural = 'Colaboradores'

