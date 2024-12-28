from django.urls import path
from . import views
from .views import lista_proforma, crear_proforma, editar_proforma, eliminar_proforma
from django.http import HttpResponse


urlpatterns = [
    
    path('', views.lista_proforma, name='lista_proforma'),
    path('crear/', views.crear_proforma, name='crear_proforma'),
    path('editar/', views.editar_proforma, name='editar_proforma'), 
    path('eliminar/<int:pk>/', views.eliminar_proforma, name='eliminar_proforma'),

]