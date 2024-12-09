from django.urls import path
from . import views

urlpatterns = [
    path('Facturacion/', views.facturacion, name='facturacion'),
    path('PrecierreCaja/', views.PrecierreCaja, name='PrecierreCaja'),
]
