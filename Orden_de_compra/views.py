from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from .models import OrdenDeCompra
from .forms import OrdenDeCompraForm  
from decimal import Decimal

from django.views.decorators.http import require_POST

def lista_ordenes(request):
    ordenes = OrdenDeCompra.objects.filter(activo=True)  # Corrige el acceso al método 'filter'
    descuentos = ['0', '5', '10', '15']
    metodos_pago = ['EFECTIVO', 'TARJETA', 'SINPE']

    if request.method == 'POST':
        form = OrdenDeCompraForm(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad']
            precio_unitario = form.cleaned_data['precio_unitario']
            descuento = form.cleaned_data['descuento']
            metodo_pago = form.cleaned_data['metodo_pago']
            
            if not (0 <= descuento <= 30):
                form.add_error('descuento', 'El descuento debe estar entre 0 y 30.')
                return render(request, 'ordenes/orden_de_compra.html', {
                    'form': form,
                    'ordenes': ordenes,
                    'descuentos': descuentos,
                    'metodos_pago': metodos_pago
                })

            if metodo_pago not in metodos_pago:
                form.add_error('metodo_pago', 'Método de pago no válido.')
                return render(request, 'ordenes/orden_de_compra.html', {
                    'form': form,
                    'ordenes': ordenes,
                    'descuentos': descuentos,
                    'metodos_pago': metodos_pago
                })

            subtotal = cantidad * precio_unitario
            total_descuento = subtotal * (descuento / Decimal(100))
            subtotal_con_descuento = subtotal - total_descuento
            total_iva = subtotal_con_descuento * (Decimal(form.cleaned_data.get('IVI', 0)) / Decimal(100))
            total = subtotal_con_descuento + total_iva
            
            orden = form.save(commit=False)
            orden.subtotal = subtotal
            orden.total = total
            orden.save()

            return redirect('lista_ordenes')
    else:
        form = OrdenDeCompraForm()

    context = {
        'ordenes': ordenes,
        'form': form,
        'descuentos': descuentos,
        'metodos_pago': metodos_pago,
    }
    return render(request, 'ordenes/orden_de_compra.html', context)


def crear_orden(request):
    descuentos = ['0', '5', '10', '15']  
    metodos_pago = ['EFECTIVO', 'TARJETA', 'SINPE'] 

    if request.method == 'POST':
        form = OrdenDeCompraForm(request.POST)
        if form.is_valid():
            
            form.save()
            return redirect('lista_ordenes')  
    else:
        form = OrdenDeCompraForm()

    
    return render(request, 'ordenes/orden_de_compra.html', {
        'form': form,
        'descuentos': descuentos,
        'metodos_pago': metodos_pago,
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
            orden.id_usuario = request.POST.get('id_usuario')
            orden.id_proveedor = request.POST.get('id_proveedor')
            orden.id_producto = request.POST.get('id_producto')
            orden.descripcion = request.POST.get('descripcion')
            orden.cantidad = request.POST.get('cantidad')
            orden.precio_unitario = request.POST.get('precio_unitario')
            orden.descuento = request.POST.get('descuento')
            orden.metodo_pago = request.POST.get('metodo_pago')
            orden.lugar_entrega = request.POST.get('lugar_entrega')
            orden.notas = request.POST.get('notas')

            orden.save()  # Guardar los cambios
            return redirect('lista_ordenes')
        except OrdenDeCompra.DoesNotExist:
            # Manejar el error de que no existe la orden
            return redirect('lista_ordenes')  # O redirigir a una página de error