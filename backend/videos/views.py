# Importaciones
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser

from http import HTTPStatus

from datetime import datetime

from videos.serializers import VideoSerializer
from videos.models import Video

from dotenv import load_dotenv

import os


class Clase1(APIView):

    parser_classes = (MultiPartParser, FormParser)
    
    def get(self, request):

        data = Video.objects.order_by('-id').all()
        datos_json = VideoSerializer(data, many = True)
        return JsonResponse({"data": datos_json.data})
    
    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"mensaje": "Video creado exitosamente."}, status=HTTPStatus.CREATED)
        
        return JsonResponse({"error": "Error al crear el video. Por favor, revisa los datos enviados."}, status=HTTPStatus.BAD_REQUEST)
    


class Clase2(APIView):
    
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request, id):
        video_instance = get_object_or_404(Video, id=id)
        serializer = VideoSerializer(video_instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"mensaje": f"Video con ID {id} actualizado exitosamente."}, status=HTTPStatus.OK)
        
        return JsonResponse(serializer.errors, status=HTTPStatus.BAD_REQUEST)
    
    def delete(self, request, id):
        try:
            # Buscar el video por su ID
            video_instance = Video.objects.get(id=id)

            # Verificar si el video tiene un archivo en el campo 'video'
            if video_instance.video:
                # Construir la ruta completa al archivo
                file_path = f'videos/{video_instance.video}'
                # Verificar si el archivo existe y eliminarlo del almacenamiento
                if default_storage.exists(file_path):
                    default_storage.delete(file_path)

            # Eliminar la instancia del modelo de la base de datos
            video_instance.delete()

            return JsonResponse({"mensaje": f"Video con ID {id} eliminado exitosamente."}, status=HTTPStatus.OK)
        except Video.DoesNotExist:
            return JsonResponse({"error": "El video no existe."}, status=HTTPStatus.NOT_FOUND)
        except Exception as e:
            return JsonResponse({"error": f"Ocurrió un error inesperado: {str(e)}"}, status=HTTPStatus.INTERNAL_SERVER_ERROR)



