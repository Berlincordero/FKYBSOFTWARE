from django.urls import path
from . import views

urlpatterns = [
    # Define tus URLs aquí
path('', views.orden_de_compra, name='orden_de_compra'),

]
