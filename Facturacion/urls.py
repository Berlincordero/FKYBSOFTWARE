from django.urls import path
from . import views
from .views import exportar_precierres_excel 
from .views import exportar_facturas_excel

urlpatterns = [
    path('Facturacion/', views.facturacion, name='facturacion'),
    path('PrecierreCaja/', views.PrecierreCaja, name='PrecierreCaja'),
    path('exportar-precierres-excel/', exportar_precierres_excel, name='export_precierres_excel'),
    path('exportar-facturas-excel/', exportar_facturas_excel, name='export_facturas_excel'),
]
