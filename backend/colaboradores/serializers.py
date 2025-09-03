# Importaciones
from rest_framework import serializers

from dotenv import load_dotenv

from colaboradores.models import Colaborador

import os

class ColaboradorSerializer(serializers.ModelSerializer):

    # Formateo de los datos
    imagen = serializers.SerializerMethodField()

    class Meta:
        model = Colaborador
        fields = ("id", "nombre", "imagen" )

    # Formateo de la imagen
    def get_imagen(self, obj):
        return f"{os.getenv('BASE_URL')}uploads/colaboradores/{obj.foto}" 