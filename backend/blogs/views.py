# Importaciones
from django.conf import settings
from django.shortcuts import render
from django.http.response import JsonResponse
from django.http import Http404
from django.utils.text import slugify
from django.utils.dateformat import DateFormat
from django.core.files.storage import FileSystemStorage

from rest_framework.views import APIView

from http import HTTPStatus

from datetime import datetime

from dotenv import load_dotenv

from blogs.serializers import BlogSerializer

from jose import jwt

from seguridad.decorators import logueado

from blogs.models import Blog
from categorias.models import Categoria

import os

# Create your views here.
class Clase1(APIView):

    def get(self, request):
        
        # Listar registros
        data = Blog.objects.order_by('-id').all()
        datos_json = BlogSerializer(data, many = True)
        return JsonResponse({"data": datos_json.data})
    
    @logueado()
    def post(self, request):

        # Validaciones
        if request.data.get("nombre") == None or not request.data["nombre"]:
            return JsonResponse({"estado": "error", "mensaje": "El campo nombre es obligatorio."}, 
                                status = HTTPStatus.BAD_REQUEST)
        
        if request.data.get("descripcion") == None or not request.data["descripcion"]:
            return JsonResponse({"estado": "error", "mensaje": "El campo descripcion es obligatorio."}, 
                                status = HTTPStatus.BAD_REQUEST)
        
        if request.data.get("categoria_id") == None or not request.data["categoria_id"]:
            return JsonResponse({"estado": "error", "mensaje": "El campo categoria es obligatorio."}, 
                                status = HTTPStatus.BAD_REQUEST)
        
        # Que exista la categoria
        try:
            Categoria.objects.filter(id = request.data["categoria_id"]).get()
        except Categoria.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "El campo categoria no existe."}, 
                                status = HTTPStatus.BAD_REQUEST)

        # Que no se repitan los titulos del blog
        if Blog.objects.filter(nombre = request.data.get("nombre")).exists():
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
        
        # Generar url del documento en caso de que se suba
        documento = None
        if 'documento' in request.FILES:
            doc_file = request.FILES["documento"]

            # Validacion MIME
            if doc_file.content_type != "application/pdf":
                return JsonResponse({"estado": "error", "mensaje": "El documento solo puede ser pdf."}, 
                                    status = HTTPStatus.BAD_REQUEST)
            
            documento = f"{datetime.timestamp(datetime.now())}{os.path.splitext(str(request.FILES['documento']))[1]}"
            fs.save(f"blogs/{documento}", request.FILES['documento'])
        
        # Validacion MIME
        if request.FILES["foto"].content_type == "image/jpeg" or request.FILES["foto"].content_type == "image/png":

            # Subir foto
            try:
                fs.save(f"blogs/{foto}", request.FILES['foto'])
                #fs.url(request.FILES['foto'])
                fs.url(f"blogs/{foto}")  
            except:
                return JsonResponse({"estado": "error", "mensaje": "Debe de adjuntar una foto en el campo foto"}, 
                                    status = HTTPStatus.BAD_REQUEST)

            # Asociar usuario al blog
            header = request.headers.get('Authorization').split(" ")
            resuelto = jwt.decode(header[1], settings.SECRET_KEY, algorithms = [ 'HS512'])

            # Creacion del registro
            try:
                Blog.objects.create(nombre = request.data["nombre"], descripcion = request.data["descripcion"], 
                                    categoria_id = request.data["categoria_id"], fecha = datetime.now(), foto = foto, documento = documento, 
                                    user_id = resuelto["id"])
                
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
            data = Blog.objects.filter(id = id).get()
            return JsonResponse({"data": {"id": data.id, "nombre": data.nombre, "slug": data.slug, 
                                          "descripcion": data.descripcion, "fecha": DateFormat(data.fecha).format('d/m/Y'), 
                                          "categoria_id": data.categoria_id, "categoria": data.categoria.nombre, 
                                          "imagen": f"{os.getenv("BASE_URL")}uploads/blogs/{data.foto}", 
                                          "documento": f"{os.getenv("BASE_URL")}uploads/blogs/{data.documento}", 
                                          "user_id": data.user_id, "user": data.user.first_name}}, 
                                          status = HTTPStatus.CREATED)

        except Blog.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "Recurso no disponible."}, 
                                status = HTTPStatus.NOT_FOUND)


    @logueado()
    def put(self, request, id):

        # Validacion de la id
        try:
            data = Blog.objects.filter(id = id).get()

        except Blog.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "Recurso no disponible."}, 
                                status = HTTPStatus.NOT_FOUND)
        
        # Validaciones generales
        if request.data.get("nombre") == None or not request.data["nombre"]:
            return JsonResponse({"estado": "error", "mensaje": "El campo nombre es obligatorio."}, 
                                status = HTTPStatus.BAD_REQUEST)
        
        if request.data.get("descripcion") == None or not request.data["descripcion"]:
            return JsonResponse({"estado": "error", "mensaje": "El campo descripcion es obligatorio."}, 
                                status = HTTPStatus.BAD_REQUEST)
        
        if request.data.get("categoria_id") == None or not request.data["categoria_id"]:
            return JsonResponse({"estado": "error", "mensaje": "El campo categoria es obligatorio."}, 
                                status = HTTPStatus.BAD_REQUEST)
        
        # Que exista la categoria
        try:
            Categoria.objects.filter(id = request.data["categoria_id"]).get()
        except Categoria.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "El campo categoria no existe."}, 
                                status = HTTPStatus.BAD_REQUEST)

        # Modificar registro
        try:
            Blog.objects.filter(id = id).update(nombre = request.data["nombre"], slug = slugify(request.data["nombre"]),
                                                descripcion = request.data["descripcion"], categoria_id = request.data["categoria_id"])
            return JsonResponse({"estado": "ok", "mensaje": "Se modifico el registo exitosamente."}, 
                                status = HTTPStatus.OK)

        except Exception as e:
            return JsonResponse({"estado": "error", "mensaje": "Ocurrio un error inseperado"}, 
                                status = HTTPStatus.NOT_FOUND)

    @logueado()
    def delete(self, request, id):

        # Validacion de la id
        try:
            data = Blog.objects.filter(id = id).get()

        except Blog.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "Recurso no disponible."}, 
                                status = HTTPStatus.NOT_FOUND)

        # Borrar foto de la carpeta
        os.remove(f"./uploads/blogs/{data.foto}")

        # Borrar documento de la carpeta
        os.remove(f"./uploads/blogs/{data.documento}")

        # Borrar el registro de la bd
        Blog.objects.filter(id = id).delete()

        return JsonResponse({"estado": "ok", "mensaje": "Se elmino el registro exitosamente."}, 
                                status = HTTPStatus.OK)

