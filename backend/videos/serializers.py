# importaciones
from django.core.files.storage import default_storage
from rest_framework import serializers

from datetime import datetime

from dotenv import load_dotenv

from videos.models import Video


import os
import re

class VideoSerializer(serializers.ModelSerializer):
    id_youtube = serializers.CharField(required=False, allow_blank=True)
    video = serializers.FileField(required=False)
    #video = serializers.CharField(required=False, allow_blank=True)
    video_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Video
        fields = ("id", "nombre", "descripcion", "id_youtube", "video", "video_url")

    def get_video_url(self, obj):
        if obj.id_youtube:
            youtube_regex = (
                r'(https?://)?(www\.)?'
                '(youtube|youtu|youtube-nocookie)\.(com|be)/'
                '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
            
            match = re.match(youtube_regex, obj.id_youtube)
            
            if match:
                video_id = match.group(6)
                return f"https://www.youtube.com/embed/{video_id}"
            else:
                return f"https://www.youtube.com/embed/{obj.id_youtube}"
        elif obj.video:
            load_dotenv()
            base_url = os.getenv('BASE_URL')
            return f"{base_url}uploads/videos/{obj.video}"
        return None

    def validate_id_youtube(self, value):
        if not value:
            return None
        
        youtube_regex = (
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

        match = re.match(youtube_regex, value)

        if match:
            video_id = match.group(6)
            return video_id
        
        if len(value) == 11:
            return value
        
        raise serializers.ValidationError("El link o ID de YouTube no es válido.")
    
    
    def create(self, validated_data):
        # Sobreescribimos el método create para manejar la subida de archivos
        # y renombrarlos antes de guardarlos.
        video_file = validated_data.pop('video', None)

        if video_file:
            # Generamos un nombre único usando un timestamp
            timestamp = datetime.now().timestamp()
            ext = os.path.splitext(video_file.name)[1]
            filename = f'{timestamp}{ext}'
            
            # Guardamos el archivo con el nuevo nombre
            video_file_path = default_storage.save(f'videos/{filename}', video_file)
            
            # Asignamos el nombre del archivo al campo del modelo
            validated_data['video'] = os.path.basename(video_file_path)

        # Llamamos al método create del padre para guardar la instancia
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Sobreescribimos el método update para manejar la actualización del archivo
        video_file = validated_data.pop('video', None)

        if video_file:
            # Eliminar el archivo de video anterior si existe
            if instance.video and default_storage.exists(f'videos/{instance.video}'):
                default_storage.delete(f'videos/{instance.video}')
            
            # Generar un nombre único con timestamp para el nuevo archivo
            timestamp = datetime.now().timestamp()
            ext = os.path.splitext(video_file.name)[1]
            filename = f'{timestamp}{ext}'
            
            # Guardar el nuevo archivo con el nombre único
            video_file_path = default_storage.save(f'videos/{filename}', video_file)
            
            # Asignar el nuevo nombre del archivo al campo del modelo
            validated_data['video'] = os.path.basename(video_file_path)

        # Llamar al método update del padre para guardar los datos restantes
        return super().update(instance, validated_data)
