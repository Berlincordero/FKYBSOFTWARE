from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.lista_proforma, name='lista_proforma'),
    path('crear/', views.crear_proforma, name='crear_proforma'),
    path('editar/<int:pk>/', views.editar_proforma, name='editar_proforma'),   
    path('eliminar/<int:pk>/', views.eliminar_proforma, name='eliminar_proforma'),
    
]