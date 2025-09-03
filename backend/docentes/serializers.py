# Importaciones
from rest_framework import serializers

from dotenv import load_dotenv

from docentes.models import Docente

import os

class DocenteSerializer(serializers.ModelSerializer):

    # Formateo de los datos
    imagen = serializers.SerializerMethodField()

    class Meta:
        model = Docente
        fields = ("id", "nombre", "area", "imagen" )

    # Formateo de la imagen
    def get_imagen(self, obj):
        return f"{os.getenv('BASE_URL')}uploads/docentes/{obj.foto}" 
    
    



