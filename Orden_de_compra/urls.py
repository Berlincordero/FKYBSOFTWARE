# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('ordenes/', views.lista_ordenes, name='lista_ordenes'),
    path('ordenes/crear/', views.crear_orden, name='crear_orden'), 
    path('ordenes/eliminar/', views.eliminar_orden, name='eliminar_orden'),  # Nueva ruta para eliminar orden
    path('ordenes/editar/', views.editar_orden, name='editar_orden'),  # Nueva ruta para editar orden

]