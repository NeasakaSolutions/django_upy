# Importaciones
from rest_framework import serializers

from dotenv import load_dotenv

from laboratorios.models import Laboratorio

import os

class LaboratorioSerializer(serializers.ModelSerializer):

    # Formateo de los datos
    imagen = serializers.SerializerMethodField()

    class Meta:
        model = Laboratorio
        fields = ("id", "nombre", "descripcion", "imagen" )

    # Formateo de la imagen
    def get_imagen(self, obj):
        return f"{os.getenv('BASE_URL')}uploads/laboratorios/{obj.foto}" 