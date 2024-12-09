from django.urls import path
from . import views

urlpatterns = [
    
    path('Cajaregistradora/', views.Cajaregistradora_view, name='Cajaregistradora_view'),
    path('guardar_factura/', views.guardar_factura, name='guardar_factura'),
    path('abrir_caja/', views.abrir_caja_view, name='abrir_caja_view'),
]