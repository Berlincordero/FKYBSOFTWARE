from django.contrib import admin
from django.urls import include, path
from Usuarios import views as usuarios_views
from . import views

urlpatterns = [
    path('', usuarios_views.external_login, name='external_login'),
    path('index/', views.index, name="index"),
    path('admin/', admin.site.urls),
    path('terminal/', views.pos_view, name='pos_view'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('usuarios/', include('Usuarios.urls')),
]