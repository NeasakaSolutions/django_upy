# Importaciones
from django.urls import path

from seguridad.views import Clase1
from seguridad.views import Clase2
from seguridad.views import Clase3

urlpatterns = [
    path('seguridad/registro', Clase1.as_view()),
    path('seguridad/verificacion/<str:token>', Clase2.as_view()),
    path('seguridad/login', Clase3.as_view()),
]