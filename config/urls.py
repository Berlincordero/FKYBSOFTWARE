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
    path('', include("django.contrib.auth.urls")),
    
]
