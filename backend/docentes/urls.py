# Importaciones
from django.urls import path

from docentes.views import Clase1
from docentes.views import Clase2

urlpatterns = [
    path('docentes', Clase1.as_view()),
    path('docentes/<int:id>', Clase2.as_view())
]