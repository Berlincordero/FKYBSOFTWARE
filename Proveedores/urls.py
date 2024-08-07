from django.urls import path
from . import views


urlpatterns = [
    path('', views.proveedor_list, name='proveedor_list'),
    
]

