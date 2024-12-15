from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages

from Usuarios.models import CustomUser
from .forms import AgregarPersonalForm, EditarPersonalForm, CambiarContrasenaForm
from config.forms import LoginForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password



# Define el modelo de usuario configurado
User = get_user_model()

# Vista de inicio de sesión
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

# Vista de cierre de sesión
def logout_view(request):
    logout(request)
    return redirect('external_login')

# Vista de gestión de usuarios
@login_required
def usuarios(request):
    users = User.objects.filter(is_active=True)  
    return render(request, 'Usuarios/usuarios.html', {'users': users, 'current_user': request.user})

# Vista para editar personal
@login_required
def editar_personal(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = EditarPersonalForm(request.POST, instance=user, request_user=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "La información del usuario se ha actualizado correctamente.")
            return redirect('usuarios')
        else:
            if 'role' in form.errors:
                messages.error(request, "No puedes cambiar tu propio rol.")
            elif any(field in form.errors for field in ['username', 'first_name', 'last_name', 'email']):
                messages.error(request, "No puedes cambiar tus propios datos personales.")
            else:
                messages.error(request, "Por favor, corrija los errores en el formulario.")
    else:
        form = EditarPersonalForm(instance=user, request_user=request.user)

    return render(request, "Usuarios/usuarios.html", {
        "form": form,
        "users": User.objects.filter(is_active=True),
    })


@login_required
def agregar_personal(request):
    users = User.objects.filter(is_active=True) 
    if request.method == 'POST':
        form = AgregarPersonalForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            confirm_password = request.POST.get('confirm_password')
            email = form.cleaned_data.get('email')
            role = form.cleaned_data.get('role')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'El correo electrónico ya está en uso.')
            elif password != confirm_password:
                messages.error(request, 'Las contraseñas no coinciden.')
            else:
                user = form.save(commit=False)
                user.set_password(password)
                user.role = role  
                user.save()
                messages.success(request, 'Personal agregado exitosamente.')
                return redirect('usuarios')  
        else:
            messages.error(request, 'Hubo un problema al agregar al usuario. Asegúrese de que las contraseñas coinciden y que el correo electrónico no está ya registrado.')
    else:
        form = AgregarPersonalForm()
    
    return render(request, 'Usuarios/usuarios.html', {'form': form, 'users': users})
@login_required
def eliminar_personal(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == "POST":
        if request.user != user:  
            user.is_active = False
            user.save()
            messages.success(request, 'Usuario desactivado correctamente.')
        else:
            messages.error(request, 'No puedes desactivar tu propio usuario.')
        return redirect('usuarios')  
    return redirect('usuarios')
    

@login_required
def perfil_usuario(request):
    user = request.user
    is_admin = user.groups.filter(name='Admin').exists()  
    return render(request, 'Usuarios/perfil.html', {'user': user, 'is_admin': is_admin})


@login_required
def cambiar_contrasena(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    # Verificar que el usuario actual no pueda cambiar su propia contraseña aquí si es necesario
    if request.user == user:
        messages.error(request, "No puedes cambiar tu propia contraseña.")
        return redirect('usuarios')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not new_password or not confirm_password:
            messages.error(request, "Por favor, completa ambos campos de contraseña.")
            return redirect('usuarios')

        if new_password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('usuarios')

        # Actualizar la contraseña del usuario
        user.password = make_password(new_password)
        user.save()

        messages.success(request, "La contraseña se ha actualizado correctamente.")
        return redirect('usuarios')

    return redirect('usuarios')