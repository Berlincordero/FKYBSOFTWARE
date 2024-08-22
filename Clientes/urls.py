from django.urls import path
from . import views

urlpatterns = [
    
    path('Clientes/', views.modulo_cliente, name='modulo_cliente'),
    
]