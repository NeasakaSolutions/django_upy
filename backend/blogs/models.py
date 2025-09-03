# Importaciones
from django.contrib.auth.models import User
from django.db import models
from autoslug import AutoSlugField

from categorias.models import Categoria

# Create your models here.
class Blog(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, default = 1)
    categoria = models.ForeignKey(Categoria, models.DO_NOTHING, default = 1)
    nombre = models.CharField(max_length = 100, null = False)
    slug = AutoSlugField(populate_from = 'nombre', max_length = 100)
    foto = models.CharField(max_length = 100, null = True)
    descripcion = models.TextField()
    documento = models.CharField(max_length = 100, null = True)
    fecha = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'blogs'
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'