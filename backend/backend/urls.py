# Importaciones
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions

from drf_yasg.views import get_schema_view 
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title = 'Pagina segura UPY',
        default_version = 'v1',
        description = 'Api desarrollada para implementacion de backend, para una pagina segura',
        contact = openapi.Contact(email = "satou.matsuzaka.3443@gmail.com"),
        license = openapi.License(name = "BSD License"),
    ),

    public = True,
    permission_classes =(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('api/v1/', include('categorias.urls')),
    path('api/v1/', include('blogs.urls')),
    path('api/v1/', include('contacto.urls')),
    path('api/v1/', include('seguridad.urls')),
    path('api/v1/', include('blogs_helper.urls')),
    path('api/v1/', include('portadas.urls')),
    path('api/v1/', include('docentes.urls')),
    path('api/v1/', include('laboratorios.urls')),
    path('api/v1/', include('colaboradores.urls')),
    path('api/v1/', include('videos.urls')),
    path('documentacion<format>/', schema_view.without_ui(cache_timeout = 0), name = 'schema-json'),
    path('documentacion/', schema_view.with_ui('swagger', cache_timeout = 0), name = 'schema-redoc'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout = 0), name = 'schema-redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)