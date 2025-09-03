# Importaciones
from django.urls import path

from categorias.views import Clase1
from categorias.views import Clase2

urlpatterns = [
    path('categorias', Clase1.as_view()),
    path('categorias/<int:id>', Clase2.as_view()),
]

