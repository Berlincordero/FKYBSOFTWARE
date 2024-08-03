from django.urls import path
from . import views

urlpatterns = [
    path('', views.proveedor_list, name='proveedor_list'),
    path('<int:pk>/', views.proveedor_detail, name='proveedor_detail'),
    path('new/', views.proveedor_new, name='proveedor_new'),
    path('<int:pk>/edit/', views.proveedor_edit, name='proveedor_edit'),
    path('<int:pk>/delete/', views.proveedor_delete, name='proveedor_delete'),
]
