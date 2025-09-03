# Importaciones
from django.urls import path
from django.urls import include

from home.views import home_inicio

urlpatterns = [
    path('', home_inicio)
]

