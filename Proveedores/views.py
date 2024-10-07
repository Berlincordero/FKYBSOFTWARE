
from django.shortcuts import render, redirect, get_object_or_404
from .models import Proveedor
from .forms import ProveedorForm


def proveedor_list(request):
    proveedores = Proveedor.objects.all()  
    return render(request, 'proveedores/proveedor_list.html', {'proveedores': proveedores})

def agregar_proveedor(request):
    if request.method == 'POST':
        nombre_empresa = request.POST.get('nombre_empresa')
        tipo_identificacion = request.POST.get('tipo_identificacion')
        identificacion = request.POST.get('identificacion')
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        provincia = request.POST.get('provincia')
        canton = request.POST.get('canton')
        distrito = request.POST.get('distrito')
        direccion_exacta = request.POST.get('direccion')
        telefono1 = request.POST.get('telefono1')
        telefono2 = request.POST.get('telefono2')

        #Crea y guardaa
        Proveedor.objects.create(
            nombre_empresa=nombre_empresa,
            tipo_identificacion=tipo_identificacion,
            identificacion=identificacion,
            nombre=nombre,
            email=email,
            provincia=provincia,
            canton=canton,
            distrito=distrito,
            direccion_exacta=direccion_exacta,
            telefono1=telefono1,
            telefono2=telefono2
        )
        return redirect('proveedor_list')
    
def eliminar_proveedor(request):
    if request.method == 'POST':
        proveedor_id = request.POST.get('id')
        proveedor = get_object_or_404(Proveedor, id_proveedor=proveedor_id)
        proveedor.delete()
        return redirect('proveedor_list')
    

