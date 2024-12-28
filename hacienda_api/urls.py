from django.urls import path
from .views import buscar_cliente

urlpatterns = [
    path('buscar-cliente/', buscar_cliente, name='buscar_cliente'),
]