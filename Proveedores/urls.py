from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.proveedor_list, name='proveedor_list'),
    path('agregar/', views.agregar_proveedor, name='agregar_proveedor'),
    path('eliminar/', views.eliminar_proveedor, name='eliminar_proveedor'),
    path('editar/', views.editar_proveedor, name='editar_proveedor'),    
]
