# Importaciones
from django.core.files.storage import FileSystemStorage
from django.http.response import JsonResponse

from rest_framework.views import APIView

from http import HTTPStatus

from datetime import datetime

from dotenv import load_dotenv

from laboratorios.models import Laboratorio
from laboratorios.serializers import LaboratorioSerializer

import os


class Clase1(APIView):
    
    def get(self, request):
        data = Laboratorio.objects.order_by('-id').all()
        datos_json = LaboratorioSerializer(data, many = True)
        return JsonResponse({"data": datos_json.data})
    
    def post(self, request):

        # Validaciones
        if request.data.get("nombre") == None or not request.data["nombre"]:
            return JsonResponse({"estado": "error", "mensaje": "El campo nombre es obligatorio."}, 
                                status = HTTPStatus.BAD_REQUEST)
        
        if request.data.get("descripcion") == None or not request.data["descripcion"]:
            return JsonResponse({"estado": "error", "mensaje": "El campo descripcion es obligatorio."}, 
                                status = HTTPStatus.BAD_REQUEST)
        
        # Que no se repitan los laboratorios
        if Laboratorio.objects.filter(nombre = request.data.get("nombre")).exists():
            return JsonResponse({"estado": "error", "mensaje": f"El nombre {request.data["nombre"]} no esta disponible."}, 
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
                fs.save(f"laboratorios/{foto}", request.FILES['foto'])
                #fs.url(request.FILES['foto'])
                fs.url(f"laboratorios/{foto}")  
            except:
                return JsonResponse({"estado": "error", "mensaje": "Debe de adjuntar una foto en el campo foto"}, 
                                    status = HTTPStatus.BAD_REQUEST)
            
            # Creacion del registro
            try:
                Laboratorio.objects.create(nombre = request.data["nombre"], descripcion = request.data["descripcion"], 
                                       foto = foto)
                
                return JsonResponse({"estado": "ok", "mensaje": "Se creo el registro correctamente."}, 
                                    status = HTTPStatus.OK)
            except Exception as e:
                raise 404
            
        return JsonResponse({"estado": "error", "mensaje": "La foto solo puede ser png y jpg."}, 
                            status = HTTPStatus.BAD_REQUEST)


class Clase2(APIView):
    
    def put(self, request, id):

        # Validar que la id exista:
        try:
            data = Laboratorio.objects.filter(id = id).get()

        except Laboratorio.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "Recurso no disponible"}, 
                                status = HTTPStatus.NOT_FOUND)
        
        # Validaciones generales:
        if request.data.get("nombre") == None or not request.data["nombre"]:
            return JsonResponse({"estado": "error", "mensaje": "El campo nombre es obligatorio."}, 
                                status = HTTPStatus.BAD_REQUEST)
        
        if request.data.get("descripcion") == None or not request.data["descripcion"]:
            return JsonResponse({"estado": "error", "mensaje": "El campo descripcion es obligatorio."}, 
                                status = HTTPStatus.BAD_REQUEST)
        
        # Modificar la foto:
        foto_actualizada = None

        if 'foto' in request.FILES:
            try:
                fs = FileSystemStorage()
                anterior = data.foto if data.foto else None

                foto_nombre = f"{datetime.timestamp(datetime.now())}{os.path.splitext(str(request.FILES['foto']))[1]}"

                # Validar el tipo MIME
                if request.FILES["foto"].content_type not in ["image/jpeg", "image/png"]:

                    return JsonResponse({"estado": "error", "mensaje": "La foto solo puede ser png y jpg."},
                                        status=HTTPStatus.BAD_REQUEST)
                
                # Guardar la nueva foto
                fs.save(f"laboratorios/{foto_nombre}", request.FILES['foto'])

                # Asignar la nueva foto para la actualización
                foto_actualizada = foto_nombre
            
                # Si existía una foto anterior, la eliminamos
                if anterior:
                    os.remove(f"./uploads/laboratorios/{anterior}")

                
            except Exception as e:
                # Manejar cualquier error durante el proceso de la foto
                return JsonResponse({"estado": "error", "mensaje": f"Ocurrió un error al procesar la foto: {str(e)}"},
                                    status=HTTPStatus.BAD_REQUEST)
        
        # Modificar registro
        try:
            # Prepara los datos a actualizar:
            datos_para_actualizar = {"nombre": request.data["nombre"], "descripcion": request.data["descripcion"]}

            if foto_actualizada:
                datos_para_actualizar["foto"] = foto_actualizada

            Laboratorio.objects.filter(id = id).update(**datos_para_actualizar)

            return JsonResponse({"estado": "ok", "mensaje": "Se modifico el registro exitosamente"}, 
                                status = HTTPStatus.NOT_FOUND)
        
        except Exception as e:

            return JsonResponse({"estado": "error", "mesnaje": "Ocurrio un error inesperado"}, 
                                status = HTTPStatus.NOT_FOUND)


    def delete(self, request, id):

        try:
            # Validar que la id exista:
            data = Laboratorio.objects.filter(id = id).get()


        except Laboratorio.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "Recurso no disponible"}, 
                                status = HTTPStatus.NOT_FOUND)
        
        # Borrar foto de la carpeta
        os.remove(f"./uploads/laboratorios/{data.foto}")

        # Borrar el registro de la bd
        Laboratorio.objects.filter(id = id).delete()

        return JsonResponse({"estado": "ok", "mensaje": "Se elmino el registro exitosamente."}, 
                                status = HTTPStatus.OK)
