from . import views
from django.contrib import admin
from django.urls import path, include  # Asegúrate de tener esta importación también


urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
]
