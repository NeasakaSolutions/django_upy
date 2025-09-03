# Importaciones
from django.shortcuts import render
from django.http.response import JsonResponse
from django.http import Http404
from django.utils.text import slugify

from rest_framework.views import APIView
from rest_framework.response import Response

from http import HTTPStatus

from categorias.models import Categoria
from blogs.models import Blog

from categorias.serializers import CategoriaSerializer

# Create your views here.
class Clase1(APIView):
    
    def get(self, request):

        data = Categoria.objects.order_by('-id').all()
        datos_json = CategoriaSerializer(data, many = True)
        return Response({"data": datos_json.data}, status = HTTPStatus.OK)

    
    def post(self, request):

        # Validaciones
        if request.data.get("nombre") == None or not request.data.get("nombre"):
            return JsonResponse({"estado": "error", "mensaje": "El campo nombre es obligatorio."}, 
                                status = HTTPStatus.BAD_REQUEST)
        
        try:
            Categoria.objects.create(nombre = request.data['nombre'])
            return JsonResponse({"estado": "ok", "mensaje": "Se creo el registro correctamente."}, 
                                status = HTTPStatus.CREATED)
        except Exception as e:
            raise Http404
    

class Clase2(APIView):
    
    def get(self, request, id):

        try:
            data = Categoria.objects.filter(id = id).get()
            return JsonResponse({"data": {"id": data.id, "nombre": data.nombre, "slug": data.slug}}, 
                                status = HTTPStatus.OK)
        except Categoria.DoesNotExist:
            raise Http404


    def put(self, request, id):
        
        # Validaciones
        if request.data.get("nombre") == None or not request.data.get("nombre"):
            return JsonResponse({"estado": "error", "mensaje": "El campo nombre es obligatorio."}, 
                                status = HTTPStatus.BAD_REQUEST)
        
        try:
            data = Categoria.objects.filter(id = id).get()
            Categoria.objects.filter(id = id).update(nombre = request.data.get("nombre"), 
                                                     slug = slugify(request.data.get("nombre")))
            
            return JsonResponse({"estado": "ok", "mensaje": "Se modifico el registro correctamente."}, 
                                status = HTTPStatus.OK)
        except Categoria.DoesNotExist:
            raise Http404
        
    
    def delete(self, request, id):

        # Validar id
        try:
            data = Categoria.objects.filter(id = id).get()

        except Categoria.DoesNotExist:
            raise Http404
        
        if Blog.objects.filter(categoria_id = id).exists():
            return JsonResponse({"estado": "error", "mensaje": "Ocurrio un error inesperado."}, 
                                status = HTTPStatus.BAD_REQUEST)
        # Eliminar registro
        Categoria.objects.filter(id = id).delete()
            
        return JsonResponse({"estado": "ok", "mensaje": "Se elimino el registro correctamente."}, 
                                status = HTTPStatus.OK)


