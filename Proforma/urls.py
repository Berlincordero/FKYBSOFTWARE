from django.urls import path
from . import views

urlpatterns = [
    
    path('Proforma/', views.proforma_view, name='proforma_view'),
    
]