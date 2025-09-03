# Importaciones
from django.db import models

# Create your models here.
class Docente(models.Model):
    nombre = models.CharField(max_length = 100, null = False)
    area = models.TextField()
    foto = models.CharField(max_length = 100, null = True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'docentes'
        verbose_name = 'Docente'
        verbose_name_plural = 'Docentes'