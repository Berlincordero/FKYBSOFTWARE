from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Proforma
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import subprocess
from django.shortcuts import render, redirect
from .forms import ProformaForm

# Create your views here.

def lista_proforma(request):
    proformas = Proforma.objects.filter(activo=True)
    print(proformas)
    return render(request, 'Proforma.html', {'proformas': proformas})




def editar_proforma(request, pk):
    proforma = get_object_or_404(Proforma, pk=pk)

    if request.method == 'POST':
        pk = request.POST.get('proforma_id')
        proforma = get_object_or_404(Proforma, pk=pk)
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
        # Recibir los datos del formulario
        fecha = request.POST.get('fecha')
        moneda = request.POST.get('moneda')
        cliente = request.POST.get('cliente')
        codigo_actividad_economica = request.POST.get('codigo_actividad_economica')
        medio_pago = request.POST.get('medio_pago')
        condicion_venta = request.POST.get('condicion_venta')
        detalles = request.POST.get('detalles')
        nota = request.POST.get('nota')

        # Capturar los valores calculados por JavaScript
        subtotal = float(request.POST.get('subtotal', 0))
        descuento = float(request.POST.get('descuento', 0))
        iva = float(request.POST.get('iva', 0))
        total = float(request.POST.get('total', 0))

        # Crear una nueva instancia de Proforma y guardar
        proforma = Proforma(
            fecha=fecha,
            moneda=moneda,
            cliente=cliente,
            codigo_actividad_economica=codigo_actividad_economica,
            medio_pago=medio_pago,
            condicion_venta=condicion_venta,
            detalles=detalles,
            nota=nota,
            subtotal=subtotal,
            descuento=descuento,
            iva=iva,
            total=total,
        )
        proforma.save()

        # Redirigir a la página de lista de proformas
        return redirect('lista_proforma')
    return render(request, 'Proforma.html')




def eliminar_proforma(request, pk):
    proforma = get_object_or_404(Proforma, pk=pk)
    proforma.activo = False  # Marca la proforma como inactiva
    proforma.save()
    return redirect('lista_proforma')  