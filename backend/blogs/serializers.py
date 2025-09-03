# Importaciones
from rest_framework import serializers

from dotenv import load_dotenv

from blogs.models import Blog

import os

class BlogSerializer(serializers.ModelSerializer):

    # Formateo de los datos
    categoria = serializers.ReadOnlyField(source = 'categoria.nombre')
    fecha = serializers.DateTimeField(format = "%d/%m/%Y")
    imagen = serializers.SerializerMethodField()
    documento = serializers.SerializerMethodField()
    user_fullname = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ("id", "nombre", "slug", "descripcion", "fecha", "categoria", "categoria_id", 
                  "imagen", "documento", "user_id", "user", "user_fullname")

    # Formateo de la imagen
    def get_imagen(self, obj):
        return f"{os.getenv('BASE_URL')}uploads/blogs/{obj.foto}" 
    
    # Formateo del documento
    def get_documento(self, obj):
        if obj.documento:
            return f"{os.getenv('BASE_URL')}uploads/blogs/{obj.documento}"
        return None
    
    # Nombre completo
    def get_user_fullname(self, obj):
        # Comprueba que user no sea None para evitar error
        if obj.user:
            return f"{obj.user.first_name} {obj.user.last_name}".strip()
        return ""



