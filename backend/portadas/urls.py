# Importaciones
from django.urls import path

from portadas.views import Clase1
from portadas.views import Clase2
from portadas.views import Clase3

urlpatterns = [
    path('portadas', Clase1.as_view()),
    path('portadas/<int:id>', Clase2.as_view()),
    path('portadas/editar/foto', Clase3.as_view()),
]
