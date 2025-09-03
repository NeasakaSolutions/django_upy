# Importaciones
from django.urls import path

from contacto.views import Clase1

urlpatterns = [
    path('contacto', Clase1.as_view()),
]