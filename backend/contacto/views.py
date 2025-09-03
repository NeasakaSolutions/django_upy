# Importaciones
from django.http.response import JsonResponse
from django.utils import timezone

from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from http import HTTPStatus

#from datetime import datetime

from contacto.models import Contacto

from utilidades import utilidades

# Create your views here.
class Clase1(APIView):

    @swagger_auto_schema(
            operation_description = 'Endpoint para Contacto',
            responses = {
                200: 'Success',
                400: 'Bad request',
            },
            request_body = openapi.Schema(
                type = openapi.TYPE_OBJECT,
                properties = {
                    'nombre': openapi.Schema(type = openapi.TYPE_STRING, description = 'Nombre'),
                    'correo': openapi.Schema(type = openapi.TYPE_STRING, description = 'Correo'),
                    'telefono': openapi.Schema(type = openapi.TYPE_STRING, description = 'Telefono'),
                    'mensaje': openapi.Schema(type = openapi.TYPE_STRING, description = 'Mensaje'),
                },

                required = ['nombre', 'correo', 'telefono', 'mensaje']
            )
    )
    def post(self, request):
        
        # Validaciones
        if request.data.get("nombre") == None or not request.data.get("nombre"):
            return JsonResponse({"estado": "error", "mensaje": "El campo nombre es obligatorio."}, 
                                status = HTTPStatus.BAD_REQUEST)
        if request.data.get("correo") == None or not request.data.get("correo"):
            return JsonResponse({"estado": "error", "mensaje": "El campo correo es obligatorio."}, 
                                status = HTTPStatus.BAD_REQUEST)
        if request.data.get("telefono") == None or not request.data.get("telefono"):
            return JsonResponse({"estado": "error", "mensaje": "El campo telefono es obligatorio."}, 
                                status = HTTPStatus.BAD_REQUEST)
        if request.data.get("mensaje") == None or not request.data.get("mensaje"):
            return JsonResponse({"estado": "error", "mensaje": "El campo mensaje es obligatorio."}, 
                                status = HTTPStatus.BAD_REQUEST)
        
        # Crear registro
        try:
            Contacto.objects.create(nombre = request.data["nombre"], correo = request.data["correo"], 
                                    telefono = request.data["telefono"], mensaje = request.data["mensaje"], 
                                    fecha = timezone.now())
            
            html = f'''
            <h1>Nuevo mensaje de sitio web</h1>
                <ul>
                    <li>Nombre: {request.data['nombre']}</li>
                    <li>Correo: {request.data['correo']}</li>
                    <li>Telefono: {request.data['telefono']}</li>
                    <li>Mensaje: {request.data['mensaje']}</li>
                </ul>

            '''

            utilidades.sendMail(html, "Prueba correo", request.data['correo'])
            
            return JsonResponse({"estado": "ok", "mensaje": "Se mando el correo exitosamente."}, 
                                status = HTTPStatus.OK)

        except Exception as e:
            return JsonResponse({"estado": "error", "mensaje": "Ocurrio un error inesperado"}, 
                                status = HTTPStatus.BAD_REQUEST)
        

