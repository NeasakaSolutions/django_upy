# Importaciones
from rest_framework import serializers

from portadas.models import Portada

from dotenv import load_dotenv

import os


class PortadaSerializer(serializers.ModelSerializer):
    foto = serializers.SerializerMethodField()
    

    class Meta:
        model = Portada
        fields = ("id", "seccion", "foto") 

    
    # Formateo de la imagen
    def get_foto(self, obj):
        return f"{os.getenv('BASE_URL')}uploads/portadas/{obj.foto}" 
