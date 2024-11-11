from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Proforma
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import subprocess
from django.shortcuts import render, redirect
from .models import Proforma
# Create your views here.

def lista_proforma(request):
    proformas = Proforma.objects.filter(activo=True)
    return render(request, 'Proforma.html', {'proformas': proformas})


def editar_proforma(request):
    if request.method == 'POST':
        # Obtén el pk del producto desde el formulario
        pk = request.POST.get('proforma_id')
        proforma = get_object_or_404(Proforma, pk=pk)
        
        proforma.fecha = request.POST.get('fecha')
        proforma.moneda = request.POST.get('moneda')
        proforma.cliente = request.POST.get('cliente')
        proforma.codigo_actividad_economica = request.POST.get('codigo_actividad_economica')
        proforma.medio_pago = request.POST.get('medio_pago')
        proforma.condicion_venta = request.POST.get('condicion_venta')
        proforma.detalles = request.POST.get('detalles')
        proforma.nota = request.POST.get('nota')   # Este es solo un ejemplo; reemplaza por el cálculo adecuado
        
        proforma.save()
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
        subtotal = 1000  # Este es solo un ejemplo; reemplaza por el cálculo adecuado
        descuento = 0    # Este es solo un ejemplo; reemplaza por el cálculo adecuado
        iva = 130        # Este es solo un ejemplo; reemplaza por el cálculo adecuado
        total = 1130     # Este es solo un ejemplo; reemplaza por el cálculo adecuado

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


from .models import Proforma


def eliminar_proforma(request, pk):
    proforma = get_object_or_404(Proforma, pk=pk)
    proforma.activo = False  # Marca la proforma como inactiva
    proforma.save()
    return redirect('lista_proforma')  