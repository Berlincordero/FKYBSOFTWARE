from django.urls import path
from . import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    
    path('external_login/', views.external_login, name='external_login'),
    path('', views.usuarios, name='usuarios'),
    path('logout/', views.logout_view, name='logout'),
    
]