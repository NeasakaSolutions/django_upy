# Importaciones
from django.http.response import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.utils.dateformat import DateFormat

from rest_framework.views import APIView
from rest_framework.response import Response

from http import HTTPStatus

from dotenv import load_dotenv

from datetime import datetime

from seguridad.decorators import logueado

from portadas.models import Portada
from portadas.serializers import PortadaSerializer

import os

# Clases
class Clase1(APIView):

    def get(self, request):
        
        data = Portada.objects.order_by('-id').all()
        datos_json = PortadaSerializer(data, many = True)
        return JsonResponse({"data": datos_json.data})
    
    @logueado()
    def post(self, request):

        # Validaciones
        if request.data.get("seccion") == None or not request.data["seccion"]:
            return JsonResponse({"estado": "error", "mensaje": "El campo seccion es obligatorio."}, 
                                status = HTTPStatus.BAD_REQUEST)
        
        # Funcion fs
        fs = FileSystemStorage()

        # Generar url de la imagen
        try:
            foto = f"{datetime.timestamp(datetime.now())}{os.path.splitext(str(request.FILES['foto']))[1]}"
        except Exception as e:
            return JsonResponse({"estado": "error", "mensaje": "Debe de adjuntar una foto en el campo foto."}, 
                                status = HTTPStatus.BAD_REQUEST)
        
        # Validacion MIME
        if request.FILES["foto"].content_type == "image/jpeg" or request.FILES["foto"].content_type == "image/png":

            # Subir foto
            try:
                fs.save(f"portadas/{foto}", request.FILES['foto'])
                #fs.url(request.FILES['foto'])
                fs.url(f"portadas/{foto}")  
            except:
                return JsonResponse({"estado": "error", "mensaje": "Debe de adjuntar una foto en el campo foto"}, 
                                    status = HTTPStatus.BAD_REQUEST)
            
            # Creacion del registro
            try:
                Portada.objects.create(seccion = request.data["seccion"], foto = foto)
                
                return JsonResponse({"estado": "ok", "mensaje": "Se creo el registro correctamente."}, 
                                    status = HTTPStatus.OK)
            except Exception as e:
                raise 404
            
        return JsonResponse({"estado": "error", "mensaje": "La foto solo puede ser png y jpg."}, 
                            status = HTTPStatus.BAD_REQUEST)


class Clase2(APIView):
        
    
    def get(self, request, id):

        # Mostrar registro
        try:
            data = Portada.objects.filter(id = id).get()
            return JsonResponse({"data": {"id": data.id, "seccion": data.seccion, 
                                        "imagen": f"{os.getenv('BASE_URL')}uploads/portadas/{data.foto}"}}, 
                                        status = HTTPStatus.CREATED)

        except Portada.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "Recurso no disponible."}, 
                                status = HTTPStatus.NOT_FOUND)
  


class Clase3(APIView):

    def post(self, request):

        # Validaciones
        if request.data.get("id") == None or not request.data.get("id"):
            return JsonResponse({"estado": "error", "mensaje": "El campo id es obligatorio."}, 
                                status = HTTPStatus.BAD_REQUEST)
        
        try:
            existe = Portada.objects.filter(id = request.data["id"]).get()
            anterior = existe.foto
        
        except Portada.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "La seccion no existe en la BD."}, 
                                status = HTTPStatus.BAD_REQUEST)
        
        # Funcion fs
        fs = FileSystemStorage()

        # Generar url de la imagen
        try:
            foto = f"{datetime.timestamp(datetime.now())}{os.path.splitext(str(request.FILES['foto']))[1]}"
        except Exception as e:
            return JsonResponse({"estado": "error", "mensaje": "Debe de adjuntar una foto en el campo foto."}, 
                                status = HTTPStatus.BAD_REQUEST)
        
        # Validacion MIME
        if request.FILES["foto"].content_type == "image/jpeg" or request.FILES["foto"].content_type == "image/png":

            # Subir foto
            try:
                fs.save(f"portadas/{foto}", request.FILES['foto'])
                #fs.url(request.FILES['foto'])
                fs.url(f"portadas/{foto}")  
            except:
                return JsonResponse({"estado": "error", "mensaje": "Debe de adjuntar una foto en el campo foto"}, 
                                    status = HTTPStatus.BAD_REQUEST)
            
            # Editar registro
            try:
                Portada.objects.filter(id = request.data["id"]).update(foto = foto)
                # Eliminar registro anterior
                os.remove(f"./uploads/portadas/{anterior}")

                return JsonResponse({"estado": "ok", "mensaje": "Se modifico el registro exitosamente."}, 
                                    status = HTTPStatus.OK)
            
            except Exception as e:
                return JsonResponse({"estado": "error", "mensaje": "Ocurrio un error insesperado."}, 
                                    status = HTTPStatus.BAD_REQUEST)
            
        else:
            return JsonResponse({"estado": "error", "mensaje": "La foto solo puede ser png y jpg."}, 
                                status = HTTPStatus.BAD_REQUEST)
