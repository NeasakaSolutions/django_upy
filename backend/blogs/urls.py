# Importaciones
from django.urls import path

from blogs.views import Clase1
from blogs.views import Clase2

urlpatterns = [
    path('blogs', Clase1.as_view()),
    path('blogs/<int:id>', Clase2.as_view()),
]