from django.contrib import admin
from django.urls import include, path

import Usuarios
import Usuarios.views
from . import views

urlpatterns = [
    path('', Usuarios.views.external_login, name='external_login'),
    path('index/', views.index, name="index"),
    path('admin/', admin.site.urls),
    path('terminal/', views.pos_view, name='pos_view'),
    path('producto/', views.producto_view, name='producto_view'),
    path('proforma/', views.proforma_view, name='proforma_view'),
    path('base2/', views.base2, name='base2'),
    path('', include("django.contrib.auth.urls")),
    
]
