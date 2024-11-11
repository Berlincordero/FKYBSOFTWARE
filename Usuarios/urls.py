from django.urls import path
from . import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    
    path('external_login/', views.external_login, name='external_login'),
    path('', views.usuarios, name='usuarios'),
    path('logout/', views.logout_view, name='logout'),
    path('agregar_personal/', views.agregar_personal, name='agregar_personal'),
    path('usuarios/editar_personal/<int:user_id>/', views.editar_personal, name='editar_personal'),
    path('usuarios/eliminar/<int:user_id>/', views.eliminar_personal, name='eliminar_personal'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),

    
]