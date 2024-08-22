from django.urls import path
from . import views

urlpatterns = [
    
    path('Inventario/', views.Inventario_view, name='Inventario_view'),
    
]