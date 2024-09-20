from django.urls import path
from . import views

urlpatterns = [
    path('Facturacion/', views.facturacion, name='facturacion'),
    path('FormularioATV/', views.FormularioATV, name='FormularioATV'),
    path('enviar-factura/', views.enviar_factura, name='enviar_factura'),
]
