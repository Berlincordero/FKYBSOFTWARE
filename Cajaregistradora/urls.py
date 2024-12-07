from django.urls import path
from . import views

urlpatterns = [
    
    path('Cajaregistradora/', views.Cajaregistradora_view, name='Cajaregistradora_view'),
    
    
]