from django.contrib import admin
from django.urls import include, path

from Usuarios import views as usuarios_views
import Usuarios.views
from . import views

urlpatterns = [
    path('', usuarios_views.external_login, name='external_login'),
    path('index/', views.index, name="index"),
    path('modulo_transporte/', views.modulo_transporte, name='modulo_transporte'),
    path('agregar_conductor/', views.agregar_conductor, name='agregar_conductor'),
    path('agregar_placa/', views.agregar_placa, name='agregar_placa'),
    path('asignar_ruta/', views.asignar_ruta, name='asignar_ruta'),
    path('admin/', admin.site.urls),
    path('terminal/', views.pos_view, name='pos_view'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('usuarios/', include('Usuarios.urls')),
    path('producto/', views.producto_view, name='producto_view'),
    path('proforma/', views.proforma_view, name='proforma_view'),
    path('facturacion/', views.facturacion_view, name='facturacion_view'),
    path('informacion/', views.informacion_view, name='informacion_view'),
    path('', include("django.contrib.auth.urls")),
    path('Reportes/', include('Reportes.urls')),
    path('proveedores/', include('Proveedores.urls')),  # Ruta para las URLs de la app Proveedores
    
    path('modulo_cliente/', views.modulo_cliente, name='modulo_cliente'),
]