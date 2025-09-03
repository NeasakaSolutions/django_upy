# Importaciones
from django.urls import path

from colaboradores.views import Clase1
from colaboradores.views import Clase2

urlpatterns = [
    path('colaboradores', Clase1.as_view()),
    path('colaboradores/<int:id>', Clase2.as_view())
]