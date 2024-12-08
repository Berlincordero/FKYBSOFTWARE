from django.shortcuts import render
from Cajaregistradora.models import Factura
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse


def facturacion(request):
    return render(request, 'Facturacion/facturacion.html')

def FormularioATV(request):
    return render(request, 'Facturacion/FormularioATV.html')


def Verificacioncomprobante(request):
    return render(request, 'Facturacion/Verificacioncomprobante.html')



def facturacion(request):
    facturas = Factura.objects.all()  # Obtener todas las facturas
    context = {"facturas": facturas}
    return render(request, 'Facturacion/facturacion.html', context)

