from django.urls import path
from . import views

urlpatterns = [
    
    path('Facturacion/', views.facturacion_view, name='facturacion_view'),
    
]