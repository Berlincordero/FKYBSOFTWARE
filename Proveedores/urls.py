from django.urls import path
from . import views

urlpatterns = [
    path('', views.proveedor_list, name='proveedor_list'),
    path('detail/', views.proveedor_detail, name='proveedor_detail'),
    path('new/', views.proveedor_new, name='proveedor_new'),
    path('edit/', views.proveedor_edit, name='proveedor_edit'),
    path('delete/', views.proveedor_delete, name='proveedor_delete'),
]
