# Importaciones
from django.urls import path

from videos.views import Clase1
from videos.views import Clase2

urlpatterns = [
    path('videos', Clase1.as_view()),
    path('videos/<int:id>', Clase2.as_view())
]