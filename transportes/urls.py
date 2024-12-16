# transportes/urls.py

from django.urls import path
from . import views
from .views import editar_conductor, editar_ruta, eliminar_ruta, eliminar_todas_rutas, modulo_rutas, asignar_rutas, agregar_ruta, eliminar_conductor

app_name = 'transportes'  # Agrega esta línea para definir el namespace

urlpatterns = [
    path('modulo_transportes/', views.modulo_transportes, name='modulo_transportes'),
    path('agregar_conductor/', views.agregar_conductor, name='agregar_conductor'),
    path('editar_conductor/<str:id_conductor>/', editar_conductor, name='editar_conductor'),
    path('eliminar_conductor/<str:id_conductor>/', views.eliminar_conductor, name='eliminar_conductor'),
    
    
    path('vehiculos/', views.modulo_vehiculos, name='modulo_vehiculos'),
    path('vehiculos/agregar/', views.agregar_vehiculo, name='agregar_vehiculo'),
    path('vehiculos/editar/<str:id_vehiculo>/', views.editar_vehiculo, name='editar_vehiculo'),
    path('eliminar_vehiculo/<str:id_vehiculo>/', views.eliminar_vehiculo, name='eliminar_vehiculo'),
    
    
    path('editar_conductor/', editar_conductor, name='editar_conductor'),
    path('eliminar_ruta/<str:id>/', views.eliminar_ruta, name='eliminar_ruta'),
    path('eliminar_todas_rutas/', eliminar_todas_rutas, name='eliminar_todas_rutas'),
    path('asignar_rutas/', asignar_rutas, name='asignar_rutas'),
    path('modulo_rutas/', modulo_rutas, name='modulo_rutas'),
    path('agregar_ruta/', views.agregar_ruta, name='agregar_ruta'),
    path('editar_ruta/<str:id_ruta>/', views.editar_ruta, name='editar_ruta'),
    path('asignar_rutas/', views.asignar_rutas, name='asignar_rutas'),
    






]
