from django.urls import path
from . import views

urlpatterns = [
    
    path('Informacion/', views.informacion_view, name='informacion_view'),
    
]