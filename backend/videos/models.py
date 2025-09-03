# Importaciones
from django.db import models

from categorias.models import Categoria

# Create your models here.
class Video(models.Model):
    nombre = models.CharField(max_length = 100, null = False)
    descripcion = models.TextField()
    id_youtube = models.CharField(max_length = 100, null = True)
    video = models.CharField(max_length = 100, null = True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'videos'
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'

