
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from .models import Proveedor
from .forms import ProveedorForm


def proveedor_list(request):
    proveedores = Proveedor.objects.filter(activo=True) 
    return render(request, 'proveedor_list.html', {'proveedores': proveedores})

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
        direccion_exacta = request.POST.get('direccion_exacta')
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
        proveedor.activo = False  # Marca el proveedor como inactivo
        proveedor.save()  # Guarda el cambio en la base de datos
        return redirect('proveedor_list')
    
def editar_proveedor(request):
    if request.method == 'POST':
        proveedor_id = request.POST.get('id_proveedor')
        proveedor = get_object_or_404(Proveedor, id_proveedor=proveedor_id)
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            proveedor = form.save(commit=False)  
            proveedor.activo = True  
            proveedor.save()  
            return redirect('proveedor_list') 
    return redirect('proveedor_list')
    



