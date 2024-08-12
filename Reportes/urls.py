from django.urls import path
from . import views

urlpatterns = [
    
    path('Ventas/', views.ventas, name='ventas'),
    path('CuentasCobrar/', views.cuentasCobrar, name='cuentasCobrar'),
    path('PagosFacturas/', views.pagosFacturas, name='pagosFacturas'),
    path('reporteUtilidades/', views.reporteUtilidades, name='reporteUtilidades'),
    path('cierreCaja/', views.cierreCaja, name='cierreCaja'),
    path('reporteProformas/', views.reporteProformas, name='reporteProformas'), 
    path('reportetransportes/', views.reportetransportes, name='reportetransportes'),  

]