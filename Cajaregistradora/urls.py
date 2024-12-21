from django.urls import path
from . import views

urlpatterns = [
    path('Cajaregistradora/', views.Cajaregistradora_view, name='Cajaregistradora_view'),
    path('guardar_factura/', views.guardar_factura, name='guardar_factura'),
    path('abrir_caja/', views.abrir_caja_view, name='abrir_caja_view'),
    path('guardar_movimiento_dinero/', views.guardar_movimiento_dinero, name='guardar_movimiento_dinero'),
    path('guardar_precierre/', views.guardar_precierre, name='guardar_precierre'),
    path('verificar_caja_abierta/', views.verificar_caja_abierta, name='verificar_caja_abierta'),
]



#Este Codigo tiene copyrights 2024  estructurado por Berlin Cordero Brenes