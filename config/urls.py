from django.contrib import admin
from django.urls import include, path

from Usuarios import views as usuarios_views
import Usuarios.views
from transportes.views import ConductorListView
from . import views

urlpatterns = [
    path('', usuarios_views.external_login, name='external_login'),
    path('index/', views.index, name="index"),
    path('admin/', admin.site.urls),
    path('transportes/', include('transportes.urls')),
    path('modulo_transportes/', ConductorListView.as_view(), name='modulo_transportes'),
    path('Cajaregistradora/', include('Cajaregistradora.urls')), 
    path('Inventario/', include('Inventario.urls')),  # Ruta para las URLs de la app Inventario
    path('accounts/', include("django.contrib.auth.urls")),
    path('usuarios/', include('Usuarios.urls')),
    path('Proforma/', include('Proforma.urls')),  # Ruta para las URLs de la app Proforma
    path('Facturacion/', include('Facturacion.urls')),  # Ruta para las URLs de la app Facturacion # Ruta para las URLs de la app Informacion
    path('', include("django.contrib.auth.urls")),
    path('Reportes/', include('Reportes.urls')),
    path('Proveedores/', include('Proveedores.urls')),  # Ruta para las URLs de la app Proveedores
    path('Orden_de_compra/', include('Orden_de_compra.urls')),  # Ruta para las URLs de la app Orden_de_compra
    path('clientes/', include('Clientes.urls')),
]