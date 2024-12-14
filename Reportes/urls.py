from django.urls import path
from . import views


urlpatterns = [
    
    path('Ventas/', views.ventas, name='ventas'),
    path('CuentasCobrar/', views.cuentasCobrar, name='cuentasCobrar'),
    path('PagosFacturas/', views.pagosFacturas, name='pagosFacturas'),
    path('reporteUtilidades/', views.reporteUtilidades, name='reporteUtilidades'),
    path('cierreCaja/', views.cierreCaja, name='cierreCaja'),
    path('cierreCaja/filtrar/', views.filtrar_movimientos, name='filtrar_movimientos'),
    path('reporteProformas/', views.reporteProformas, name='reporteProformas'), 
    path('reporte-transportes/', views.reporteTransportes, name='reportetransportes'),
    path('reporte-cuentas-por-cobrar/', views.generar_pdf_cuentas_por_cobrar, name='reporte_cuentas_por_cobrar'),
    path('reporte-pagos-facturas/', views.generar_pdf_pagos_facturas, name='reporte_pagos_facturas'),
    path('detalle-proforma-pdf/<int:proforma_id>/', views.generar_pdf_proforma_detalle, name='detalle_proforma_pdf'),
    path('reporte-transportes-pdf/', views.generar_pdf_transportes, name='reporte_transportes_pdf'),
    path('detallesProforma/<int:pk>/', views.detalles_proforma, name='detalles_proforma'),
    path('descargar_reporte_ventas/', views.descargar_reporte_ventas, name='descargar_reporte_ventas'),   
    path('descargar_factura/<str:numero_factura>/', views.descargar_factura, name='descargar_factura'),
    path('obtener_factura/<str:numero_factura>/', views.obtener_factura, name='obtener_factura'),
    path('descargar_reporte_utilidades/', views.descargar_reporte_utilidades, name='descargar_reporte_utilidades'),
    path('cierreCaja/reporte_pdf/', views.generar_pdf_cierre_caja, name='reporte_pdf_cierre'),
    

    ]