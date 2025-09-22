# Importaciones
from django.core.files.storage import FileSystemStorage
from django.http.response import JsonResponse

from rest_framework.views import APIView

from http import HTTPStatus

from datetime import datetime

from docentes.serializers import DocenteSerializer
from docentes.models import Docente

from dotenv import load_dotenv

import os

# Clases de la aplicacion
class Clase1(APIView):

    def get(self, request):
        data = Docente.objects.order_by('-id').all()
        datos_json = DocenteSerializer(data, many = True)
        return JsonResponse({"data": datos_json.data})
    
    def post(self, request):

        # Validaciones
        if request.data.get("nombre") == None or not request.data["nombre"]:
            return JsonResponse({"estado": "error", "mensaje": "El campo nombre es obligatorio."}, 
                                status = HTTPStatus.BAD_REQUEST)
        
        if request.data.get("area") == None or not request.data["area"]:
            return JsonResponse({"estado": "error", "mensaje": "El campo area es obligatorio."}, 
                                status = HTTPStatus.BAD_REQUEST)
        

        # Que no se repitan los titulos del blog
        if Docente.objects.filter(nombre = request.data.get("nombre")).exists():
            return JsonResponse({"estado": "error", "mensaje": f"El nombre {request.data['nombre']} no esta disponible."}, 
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
                fs.save(f"docentes/{foto}", request.FILES['foto'])
                #fs.url(request.FILES['foto'])
                fs.url(f"docentes/{foto}")  
            except:
                return JsonResponse({"estado": "error", "mensaje": "Debe de adjuntar una foto en el campo foto"}, 
                                    status = HTTPStatus.BAD_REQUEST)


            # Creacion del registro
            try:
                Docente.objects.create(nombre = request.data["nombre"], area = request.data["area"], 
                                       foto = foto)
                
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
            data = Docente.objects.filter(id = id).get()
            return JsonResponse({"data": {"id": data.id, "nombre": data.nombre, "area": data.area,
                                          "imagen": f"{os.getenv('BASE_URL')}uploads/docentes/{data.foto}" }}, 
                                          status = HTTPStatus.CREATED)

        except Docente.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "Recurso no disponible."}, 
                                status = HTTPStatus.NOT_FOUND)
        

    def put(self, request, id):
        
        # Validar que la id exista:
        try:
            data = Docente.objects.filter(id = id).get()

        except Docente.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "Recurso no disponible"}, 
                                status = HTTPStatus.NOT_FOUND)
        
        # Validaciones generales:
        if request.data.get("nombre") == None or not request.data["nombre"]:
            return JsonResponse({"estado": "error", "mensaje": "El campo nombre es obligatorio."}, 
                                status = HTTPStatus.BAD_REQUEST)
        
        if request.data.get("area") == None or not request.data["area"]:
            return JsonResponse({"estado": "error", "mensaje": "El campo area es obligatorio."}, 
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
                fs.save(f"docentes/{foto_nombre}", request.FILES['foto'])

                # Asignar la nueva foto para la actualización
                foto_actualizada = foto_nombre
            
                # Si existía una foto anterior, la eliminamos
                if anterior:
                    os.remove(f"./uploads/docentes/{anterior}")

                
            except Exception as e:
                # Manejar cualquier error durante el proceso de la foto
                return JsonResponse({"estado": "error", "mensaje": f"Ocurrió un error al procesar la foto: {str(e)}"},
                                    status=HTTPStatus.BAD_REQUEST)
        
        # Modificar registro
        try:
            # Prepara los datos a actualizar:
            datos_para_actualizar = {"nombre": request.data["nombre"], "area": request.data["area"]}

            if foto_actualizada:
                datos_para_actualizar["foto"] = foto_actualizada

            Docente.objects.filter(id = id).update(**datos_para_actualizar)

            return JsonResponse({"estado": "ok", "mensaje": "Se modifico el registro exitosamente"}, 
                                status = HTTPStatus.OK)
        
        except Exception as e:

            return JsonResponse({"estado": "error", "mesnaje": "Ocurrio un error inesperado"}, 
                                status = HTTPStatus.NOT_FOUND)


    def delete(self, request, id):

        try:
            # Validar que la id exista:
            data = Docente.objects.filter(id = id).get()


        except Docente.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "Recurso no disponible"}, 
                                status = HTTPStatus.NOT_FOUND)
        
        # Borrar foto de la carpeta
        os.remove(f"./uploads/docentes/{data.foto}")

        # Borrar el registro de la bd
        Docente.objects.filter(id = id).delete()

        return JsonResponse({"estado": "ok", "mensaje": "Se elmino el registro exitosamente."}, 
                                status = HTTPStatus.OK)

