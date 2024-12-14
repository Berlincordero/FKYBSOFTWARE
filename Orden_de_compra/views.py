from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from .models import OrdenDeCompra
from .forms import OrdenDeCompraForm  
from decimal import Decimal
from django.views.decorators.http import require_POST


def lista_ordenes(request):
    ordenes = OrdenDeCompra.objects.filter(activo=True)  # Filtrar órdenes activas
    metodos_pago = ['EFECTIVO', 'TARJETA', 'SINPE']  # Métodos de pago disponibles

    if request.method == 'POST':
        form = OrdenDeCompraForm(request.POST)
       
        if form.is_valid():
            
            cantidad = form.cleaned_data['cantidad']
            precio_unitario = form.cleaned_data['precio_unitario']

            # Calcular el total
            total = cantidad * precio_unitario

            # Crear la orden con los datos ingresados
            orden = form.save(commit=False)
            
            orden.total = total
            orden.save()

            return redirect('lista_ordenes')  # Redirigir a la lista de órdenes
    else:
        form = OrdenDeCompraForm()

    context = {
        'ordenes': ordenes,
        'form': form,
        'metodos_pago': metodos_pago,
    }
    return render(request, 'ordenes/orden_de_compra.html', context)



def crear_orden(request):
    metodos_pago = ['EFECTIVO', 'TARJETA', 'SINPE']  # Métodos de pago disponibles
    proveedores = Proveedor.objects.all()  # Obtener todos los proveedores

    if request.method == 'POST':
        form = OrdenDeCompraForm(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad']
            precio_unitario = form.cleaned_data['precio_unitario']

            # Calcular el total
            total = cantidad * precio_unitario

            # Crear la orden con los datos ingresados
            orden = form.save(commit=False)
        
            orden.total = total
            orden.save()
            
            return redirect('lista_ordenes')  # Redirigir a la lista de órdenes
    else:
        form = OrdenDeCompraForm()

    return render(request, 'ordenes/orden_de_compra.html', {
        'form': form,
        'metodos_pago': metodos_pago,
        'proveedores': proveedores,
    })


@require_POST
def eliminar_orden(request):
    orden_id = request.POST.get('orden_id')
    orden = get_object_or_404(OrdenDeCompra, id_orden=orden_id)
    orden.activo = False  # Marca la orden como inactiva
    orden.save()  # Guarda el cambio en la base de datos
    return redirect('lista_ordenes')

@require_POST
def editar_orden(request):
    if request.method == 'POST':
        orden_id = request.POST.get('orden_id')
        try:
            orden = OrdenDeCompra.objects.get(id_orden=orden_id)
            orden.usuario = request.user  # Asignar usuario logueado automáticamente
            orden.producto = request.POST.get('producto')
            orden.descripcion = request.POST.get('descripcion')
            orden.cantidad = int(request.POST.get('cantidad'))
            orden.precio_unitario = float(request.POST.get('precio_unitario'))
            orden.proveedor = Proveedor.objects.get(id=request.POST.get('proveedor'))
            orden.metodo_pago = request.POST.get('metodo_pago')
            orden.notas = request.POST.get('notas')

            orden.save()  # Guardar los cambios
            return redirect('lista_ordenes')
        except OrdenDeCompra.DoesNotExist:
            # Manejar el error de que no existe la orden
            return redirect('lista_ordenes')  # O redirigir a una página de error

def detalle_orden(request, orden_id):
    orden = get_object_or_404(OrdenDeCompra, id=orden_id)
    return render(request, 'ordenes/detalle_orden.html', {
        'orden': orden,    
    })