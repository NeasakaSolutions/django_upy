# Importaciones
from django.core.files.storage import FileSystemStorage
from django.http.response import JsonResponse

from rest_framework.views import APIView

from http import HTTPStatus

from datetime import datetime

from videos.serializers import VideoSerializer
from videos.models import Video

from dotenv import load_dotenv

import os


class Clase1(APIView):
    
    def get(self, request):

        data = Video.objects.order_by('-id').all()
        datos_json = VideoSerializer(data, many = True)
        return JsonResponse({"data": datos_json.data})
    
    def post(self, request):
        
        pass
    


class Clase2(APIView):
    
    pass



