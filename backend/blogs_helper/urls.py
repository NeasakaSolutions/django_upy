# Importaciones
from django.urls import path

from blogs_helper.views import Clase1
from blogs_helper.views import Clase2
from blogs_helper.views import Clase3
from blogs_helper.views import Clase4
from blogs_helper.views import Clase5
from blogs_helper.views import Clase6

urlpatterns = [
    path('blogs/editar/foto', Clase1.as_view()),
    path('blogs/slug/<str:slug>', Clase2.as_view()),
    path('blogs-home', Clase3.as_view()),
    path('blogs-panel/<int:id>', Clase4.as_view()),
    path('blogs-buscador', Clase5.as_view()),
    path('blogs/editar/documento', Clase6.as_view()),
]