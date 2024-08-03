from django.urls import path
from . import views

urlpatterns = [
    
    path('Ventas/', views.ventas, name='ventas'),
    path('CuentasCobrar/', views.cuentasCobrar, name='cuentasCobrar'),
    path('PagosFacturas/', views.pagosFacturas, name='pagosFacturas'),

]