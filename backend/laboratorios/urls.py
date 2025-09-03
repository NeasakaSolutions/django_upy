# Importaciones
from django.urls import path

from laboratorios.views import Clase1
from laboratorios.views import Clase2

urlpatterns = [
    path('laboratorios', Clase1.as_view()),
    path('laboratorios/<int:id>', Clase2.as_view())
]