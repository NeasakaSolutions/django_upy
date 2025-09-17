# Importaciones
from django.http.response import JsonResponse
from django.utils import timezone

from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from http import HTTPStatus

#from datetime import datetime

from dotenv import load_dotenv

from contacto.models import Contacto

from utilidades import utilidades

import os

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
            
            html = f"""
                <!DOCTYPE html>
                <html lang="es">
                <head>
                <meta charset="UTF-8">
                <title>Nuevo mensaje</title>
                </head>
                <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px;">
                <table align="center" width="600" cellpadding="0" cellspacing="0" 
                        style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <tr>
                    <td style="background-color: #1a73e8; color: #ffffff; text-align: center; padding: 20px;">
                        <h1 style="margin: 0; font-size: 22px;">Nuevo mensaje de la página de Ciberseguridad</h1>
                    </td>
                    </tr>
                    <tr>
                    <td style="padding: 20px; color: #333333; font-size: 14px;">
                        <p style="margin-bottom: 15px;">Has recibido un nuevo mensaje desde el formulario de contacto:</p>
                        <table width="100%" cellpadding="8" cellspacing="0" 
                            style="border-collapse: collapse; font-size: 14px;">
                        <tr style="background-color: #f9f9f9;">
                            <td style="font-weight: bold; width: 120px;">Nombre:</td>
                            <td>{request.data['nombre']}</td>
                        </tr>
                        <tr>
                            <td style="font-weight: bold;">Correo:</td>
                            <td>{request.data['correo']}</td>
                        </tr>
                        <tr style="background-color: #f9f9f9;">
                            <td style="font-weight: bold;">Teléfono:</td>
                            <td>{request.data['telefono']}</td>
                        </tr>
                        <tr>
                            <td style="font-weight: bold; vertical-align: top;">Mensaje:</td>
                            <td>{request.data['mensaje']}</td>
                        </tr>
                        </table>
                        <p style="margin-top: 20px; font-size: 12px; color: #777;">Este correo se generó automáticamente desde la página web.</p>
                    </td>
                    </tr>
                </table>
                </body>
                </html>
                """


            #utilidades.sendMail(html, "Prueba correo", request.data['correo'])
            utilidades.sendMail(html, "Nuevo correo", os.getenv("SMTP_USER"))
            
            return JsonResponse({"estado": "ok", "mensaje": "Se mando el correo exitosamente."}, 
                                status = HTTPStatus.OK)

        except Exception as e:
            return JsonResponse({"estado": "error", "mensaje": "Ocurrio un error inesperado"}, 
                                status = HTTPStatus.BAD_REQUEST)
        

