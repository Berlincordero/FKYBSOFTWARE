from django.shortcuts import render, redirect
from .models import OrdenDeCompra
from .forms import OrdenDeCompraForm  
from decimal import Decimal

def lista_ordenes(request):
    ordenes = OrdenDeCompra.objects.all()
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