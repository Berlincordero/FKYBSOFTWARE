from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('crear/', views.crear_producto, name='crear_producto'),
    path('editar/', views.editar_producto, name='editar_producto'),  
    path('eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('obtener_productos/', views.obtener_productos, name='obtener_productos'),
    path('exportar_excel/', views.exportar_productos_excel, name='exportar_productos_excel'),
    path('subir_pgsql/', views.subir_bd_pgsql, name='subir_bd_pgsql'),
]