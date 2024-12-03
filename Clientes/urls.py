from django.urls import path
from . import views
from .views import buscar_clientes

app_name = 'clientes'
urlpatterns = [
    
    path('', views.modulo_clientes, name='modulo_clientes'),
    path('eliminar_cliente/<int:id_cliente>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('agregar_cliente/', views.agregar_cliente, name='agregar_cliente'),
    path('editar_cliente/<str:id_cliente>/', views.editar_cliente, name='editar_cliente'),  # Ruta para editar cliente
    path('buscar-clientes/', buscar_clientes, name='buscar_clientes'),
]
