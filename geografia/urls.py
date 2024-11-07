#geografia/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('cargar/', views.cargar_datos, name='cargar_datos'),
    path('obtener-cantones/<int:provincia_id>/', views.obtener_cantones, name='obtener_cantones'),
    path('obtener-distritos/<int:canton_id>/', views.obtener_distritos, name='obtener_distritos'),
]
