# Importaciones
from django.conf import settings
from django.http.response import JsonResponse

from functools import wraps

from http import HTTPStatus

from jose import jwt

import time


def logueado():
    def metodo(func):
        @wraps(func)
        def _decorator(request, *args, **kwargs):
            # Recibimos el primer valor que en este caso seria el request del views.py
            req = args[0]
            # Validacion por medio del header
            if not req.headers.get('Authorization') or req.headers.get('Authorization') == None:
                return JsonResponse({"estado": "error", "mensaje": "Sin autorizacion"}, 
                                    status = HTTPStatus.UNAUTHORIZED)
            # Dividir el token para quitar el Bearer
            header = req.headers.get('Authorization').split(" ")

            # Verificar que el token sea valido
            try:
                # Decodificar token
                resuelto = jwt.decode(header[1], settings.SECRET_KEY, algorithms = [ 'HS512'])
            except Exception as e:
                return JsonResponse({"estado": "error", "mensaje": "Sin autorizacion"}, 
                                    status = HTTPStatus.UNAUTHORIZED)
            
            # Verificar el token este vigente:
            if int(resuelto["exp"]) > int(time.time()):
                return func(request, *args, **kwargs)
            else:
                return JsonResponse({"estado": "error", "mensaje": "Sin autorizacion"}, 
                                    status = HTTPStatus.UNAUTHORIZED)
        return _decorator
    return metodo

