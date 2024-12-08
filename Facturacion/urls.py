from django.urls import path
from . import views

urlpatterns = [
    path('Facturacion/', views.facturacion, name='facturacion'),
    path('FormularioATV/', views.FormularioATV, name='FormularioATV'),
    path('Verificacioncomprobante/', views.Verificacioncomprobante, name='Verificacioncomprobante'),
]
