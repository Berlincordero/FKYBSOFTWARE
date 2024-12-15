# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('ordenes/', views.lista_ordenes, name='lista_ordenes'),
    path('ordenes/eliminar/', views.eliminar_orden, name='eliminar_orden'),
    path('ordenes/editar/', views.editar_orden, name='editar_orden'),  
    path('ordenes/pdf/<int:id>/', views.descargar_orden_pdf, name='descargar_orden_pdf'),


]