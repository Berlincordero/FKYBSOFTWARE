            
from .models import Proforma,  DetalleProforma
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import subprocess
from django.shortcuts import render, redirect
from .forms import ProformaForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse



# Create your views here.

def lista_proforma(request):
    proformas = Proforma.objects.filter(activo=True)  
    return render(request, 'Proforma.html', {'proformas': proformas})




from django.shortcuts import render, get_object_or_404
from .models import Proforma, DetalleProforma

def editar_proforma(request, pk):
    proforma = get_object_or_404(Proforma, pk=pk)

    if request.method == 'POST':
        # Recibir y actualizar los datos del formulario
        proforma.fecha = request.POST.get('fecha')
        proforma.moneda = request.POST.get('moneda')
        proforma.cliente = request.POST.get('cliente')
        proforma.codigo_actividad_economica = request.POST.get('codigo_actividad_economica')
        proforma.medio_pago = request.POST.get('medio_pago')
        proforma.condicion_venta = request.POST.get('condicion_venta')
        proforma.detalles = request.POST.get('detalles')
        proforma.nota = request.POST.get('nota')
        proforma.subtotal = 1000  # Este es solo un ejemplo; reemplaza por el cálculo adecuado
        proforma.descuento = 0    # Este es solo un ejemplo; reemplaza por el cálculo adecuado
        proforma.iva = 130        # Este es solo un ejemplo; reemplaza por el cálculo adecuado
        proforma.total = 1130     # Este es solo un ejemplo; reemplaza por el cálculo adecuado

        proforma.save()
         # Redirigir a la página de lista de proformas
        return redirect('lista_proforma')
    return render(request, 'Proforma.html')


def crear_proforma(request):
    if request.method == 'POST':
        # Crear la proforma
        proforma = Proforma(
            fecha=request.POST.get('fecha'),
            moneda=request.POST.get('moneda'),
            cliente=request.POST.get('cliente'),
            codigo_actividad_economica=request.POST.get('codigo_actividad_economica'),
            medio_pago=request.POST.get('medio_pago'),
            condicion_venta=request.POST.get('condicion_venta'),
            detalles=request.POST.get('detalles'),
            nota=request.POST.get('nota'),
            subtotal=request.POST.get('subtotal'),
            descuento=request.POST.get('descuento'),
            iva=request.POST.get('iva'),
            total=request.POST.get('total'),
        )
        proforma.save()

        # Guardar los productos de detalle de la proforma
        for key, value in request.POST.items():
            if key.startswith('cantidad_'):  # Solo los campos de cantidad
                producto = key.split('_')[1]  # Extraer el nombre del producto desde el campo
                cantidad = int(value)
                descuento = float(request.POST.get(f"descuento_{producto}", 0))
                precio_unitario = float(request.POST.get(f"precio_{producto}", 0))
                total = cantidad * precio_unitario - descuento

                DetalleProforma.objects.create(
                    proforma=proforma,
                    producto=producto,
                    cantidad=cantidad,
                    descuento=descuento,
                    precio_unitario=precio_unitario,
                    total=total
                )

        return redirect('lista_proforma')  # Redirigir después de guardar la proforma

    return render(request, 'Proforma.html')

def eliminar_proforma(request, pk):
    proforma = get_object_or_404(Proforma, pk=pk)
    proforma.activo = False  # Marca la proforma como inactiva
    proforma.save()
    return redirect('lista_proforma')  