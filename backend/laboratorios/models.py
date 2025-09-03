# Importaciones
from django.db import models

# Create your models here.
class Laboratorio(models.Model):
    nombre = models.CharField(max_length = 100, null = False)
    descripcion = models.TextField()
    foto = models.CharField(max_length = 100, null = True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'laboratorios'
        verbose_name = 'Laboratorio'
        verbose_name_plural = 'Laboratorios'
