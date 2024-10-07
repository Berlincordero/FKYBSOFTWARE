from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect

from config.forms import LoginForm

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import logout

"""
def external_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            
            return redirect('index')
    else:
        form = LoginForm()

    return render(request, 'external_login.html', {'form': form})
"""


def external_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            try:
                
                user = User.objects.get(email=email)
                
                user = authenticate(username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('index') 
                else:
                    form.add_error(None, 'Email o contraseña incorrectos')
            except User.DoesNotExist:
                form.add_error(None, 'Usuario no encontrado')
    else:
        form = LoginForm()

    return render(request, 'external_login.html', {'form': form})


def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('external_login')  # Redirige a la página de inicio de sesión

def usuarios(request):
    #datos = modelo.objects.all()
    return render(request, 'Usuarios/usuarios.html')