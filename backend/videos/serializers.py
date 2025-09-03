# importaciones
from django.core.files.storage import default_storage
from rest_framework import serializers

from dotenv import load_dotenv

from videos.models import Video

import os
import re

class VideoSerializer(serializers.ModelSerializer):
    id_youtube = serializers.CharField(required=False, allow_blank=True)
    video = serializers.FileField(required=False)
    
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
    
    
