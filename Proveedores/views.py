
from django.shortcuts import render, redirect
from .models import Proveedor
from .forms import ProveedorForm

def Proveedor(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        fecha = request.POST.get('fecha')
        nombreempresa = request.POST.get('nombreempresa')
        tipoIdentificacion = request.POST.get('tipoIdentificacion')
        identificacion = request.POST.get('identificacion')
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        provincia = request.POST.get('provincia')
        canton = request.POST.get('canton')
        distrito = request.POST.get('distrito')
        direccion = request.POST.get('direccion')   
        telefono1 = request.POST.get('telefono1')
        telefono2 = request.POST.get('telefono2')

        # Crear un nuevo proveedor
        Proveedor.objects.create(
            fecha=fecha,
            nombreempresa=nombreempresa,
            tipoIdentificacion=tipoIdentificacion,
            identificacion=identificacion,
            nombre=nombre,
            email=email,
            provincia=provincia,
            canton=canton,
            distrito=distrito,
            direccion=direccion,
            telefono1=telefono1,
            telefono2=telefono2
        )
        return redirect('Proveedores')  # Redirigir para evitar el reenvío del formulario

    # Obtener todos los proveedores para listarlos
    proveedores = Proveedor.objects.all()
    return render(request, 'Proveedores/Proveedores.html', {"proveedores": proveedores})
