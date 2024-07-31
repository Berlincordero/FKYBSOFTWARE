from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views

from django.shortcuts import render, redirect

from config.forms import LoginForm

def external_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            
            return redirect('index')
    else:
        form = LoginForm()

    return render(request, 'external_login.html', {'form': form})


def usuarios(request):
    #datos = modelo.objects.all()
    return render(request, 'Usuarios/usuarios.html')