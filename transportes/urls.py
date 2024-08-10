from django.urls import path
from . import views

urlpatterns = [
    path('', views.modulo_transportes, name='modulo_transportes'),
    path('guardar_conductor/', views.guardar_conductor, name='guardar_conductor'),
    path('guardar_vehiculo/', views.guardar_vehiculo, name='guardar_vehiculo'),
    path('guardar_ruta/', views.guardar_ruta, name='guardar_ruta'),
    path('eliminar_todas_las_rutas/', views.eliminar_todas_las_rutas, name='eliminar_todas_las_rutas'),
    path('imprimir_rutas/', views.imprimir_rutas, name='imprimir_rutas'),
]
