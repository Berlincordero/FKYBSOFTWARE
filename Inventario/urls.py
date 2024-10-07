from django.urls import path
from . import views

urlpatterns = [
    
   
    path('inventario/', views.inventario, name='inventario'),
    path('exportar_productos_excel/', views.exportar_productos_excel, name='exportar_productos_excel'),
    path('subir_bd_pgsql/', views.subir_bd_pgsql, name='subir_bd_pgsql'),
    
]