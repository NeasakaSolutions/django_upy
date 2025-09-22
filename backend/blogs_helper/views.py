# Importaciones
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.utils.dateformat import DateFormat
from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import Http404

from rest_framework.views import APIView

from http import HTTPStatus

from dotenv import load_dotenv

from datetime import datetime

from seguridad.decorators import logueado

from blogs.serializers import BlogSerializer
from blogs.models import Blog

from categorias.models import Categoria

import os

# Editar foto
class Clase1(APIView):

    @logueado()
    def post(self, request):

        # Validaciones
        if request.data.get("id") == None or not request.data.get("id"):
            return JsonResponse({"estado": "error", "mensaje": "El campo id es obligatorio."}, 
                                status = HTTPStatus.BAD_REQUEST)
        
        try:
            existe = Blog.objects.filter(id = request.data["id"]).get()
            anterior = existe.foto
        
        except Blog.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "El blog no existe en la BD."}, 
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
                fs.save(f"blogs/{foto}", request.FILES['foto'])
                #fs.url(request.FILES['foto'])
                fs.url(f"blogs/{foto}")  
            except:
                return JsonResponse({"estado": "error", "mensaje": "Debe de adjuntar una foto en el campo foto"}, 
                                    status = HTTPStatus.BAD_REQUEST)
            
            # Editar registro
            try:
                Blog.objects.filter(id = request.data["id"]).update(foto = foto)
                # Eliminar registro anterior
                os.remove(f"./uploads/blogs/{anterior}")

                return JsonResponse({"estado": "ok", "mensaje": "Se modifico el registro exitosamente."}, 
                                    status = HTTPStatus.OK)
            
            except Exception as e:
                return JsonResponse({"estado": "error", "mensaje": "Ocurrio un error insesperado."}, 
                                    status = HTTPStatus.BAD_REQUEST)

        else:
            return JsonResponse({"estado": "error", "mensaje": "La foto solo puede ser png y jpg."}, 
                                status = HTTPStatus.BAD_REQUEST)


class Clase2(APIView):

    def get(self, request, slug):

        # Mostrar registro
        try:
            data = Blog.objects.filter(slug = slug).get()
            return JsonResponse({"data": {"id": data.id, "nombre": data.nombre, "slug": data.slug, 
                                          "descripcion": data.descripcion, "fecha": DateFormat(data.fecha).format('d/m/Y'), 
                                          "categoria_id": data.categoria_id, "categoria": data.categoria.nombre, 
                                          "imagen": f"{os.getenv('BASE_URL')}uploads/blogs/{data.foto}", 
                                          "documento": f"{os.getenv('BASE_URL')}uploads/blogs/{data.documento}", 
                                          "user_id": data.user_id, "user": data.user.first_name}}, 
                                          status = HTTPStatus.CREATED)

        except Blog.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "Recurso no disponible."}, 
                                status = HTTPStatus.NOT_FOUND)


class Clase3(APIView):

    def get(self, request):

        #data = Blog.objects.order_by('-id').all()[:3] # Ultimos 3 blogs agregados
        data = Blog.objects.order_by('?').all()[:6] # Random 3 blogs
        datos_json = BlogSerializer(data, many = True)

        return JsonResponse({"data": datos_json.data}, status = HTTPStatus.OK)



class Clase4(APIView):

    @logueado()
    def get(self, request, id):
        
        # Validar usuario:
        try:
            existe = User.objects.filter(id = id).get()

        except User.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "Ocurrio un error inesperado."}, 
                                status = HTTPStatus.BAD_REQUEST)
        
        # Listar registros asociados a un usuario
        data = Blog.objects.filter(user_id = id).order_by('-id').all()
        datos_json = BlogSerializer(data, many = True)
        return JsonResponse({"data": datos_json.data}, status = HTTPStatus.OK)

class Clase5(APIView):

    def get(self, request):

        # Validaciones
        if request.GET.get("categoria_id") == None or not request.GET.get("categoria_id"):
            return JsonResponse({"estado": "error", "mensaje": "Ocurrio un error inesperado."}, 
                                status = HTTPStatus.BAD_REQUEST)
        
        try:
            existe = Categoria.objects.filter(id = request.GET.get("categoria_id")).get()
        
        except Categoria.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "Ocurrio un error inesperado."}, 
                                status = HTTPStatus.BAD_REQUEST)
        
        data = Blog.objects.filter(categoria_id = request.GET.get("categoria_id")).filter(nombre__icontains = request.GET.get('search')).order_by('-id').all()
        datos_json = BlogSerializer(data, many = True)

        return JsonResponse({"data": datos_json.data}, status = HTTPStatus.OK)

# Editar o agregar documento
class Clase6(APIView):

    @logueado()
    def post(self, request):

        # Validaciones
        if request.data.get("id") == None or not request.data.get("id"):
            return JsonResponse({"estado": "error", "mensaje": "El campo id es obligatorio."}, 
                                status = HTTPStatus.BAD_REQUEST)
        
        try:
            existe = Blog.objects.filter(id = request.data["id"]).get()
            anterior = existe.documento
        
        except Blog.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "El blog no existe en la BD."}, 
                                status = HTTPStatus.BAD_REQUEST)
        
        # Verificar si se envio un documento
        if "documento" not in request.FILES:
            return JsonResponse({"estado": "error", "mensaje": "Debe de adjuntar un documento PDF."}, 
                   status = HTTPStatus.BAD_REQUEST)
        
        doc_file = request.FILES["documento"]

        # Validacion MIME
        ext = os.path.splitext(doc_file.name)[1].lower()
        if doc_file.content_type != "application/pdf" or ext != ".pdf":
            return JsonResponse({"estado": "error", "mensaje": "El documento solo puede ser pdf."}, 
                                status = HTTPStatus.BAD_REQUEST)

        fs = FileSystemStorage()
        # Generar url
        documento = f"{datetime.timestamp(datetime.now())}{os.path.splitext(str(request.FILES['documento']))[1]}"
        # Guardar documento
        fs.save(f"blogs/{documento}", request.FILES['documento'])


        # Actualizar registro
        try:
            Blog.objects.filter(id=request.data["id"]).update(documento=documento)

            # En caso de que exista un documento anterior eliminar
            if anterior:
                try:
                    os.remove(f"./uploads/blogs/{anterior}")

                except FileNotFoundError:
                    pass
            
            return JsonResponse({"estado": "ok", "mensaje": "Se modifico el registro exitosamente."}, 
                                status = HTTPStatus.OK)
             
        except:
            return JsonResponse({"estado": "error", "mensaje": "Debe de adjuntar un documento en el campo documento"}, 
                                    status = HTTPStatus.BAD_REQUEST)
            
        
