from django.shortcuts import render

def facturacion(request):
    return render(request, 'Facturacion/facturacion.html')

def FormularioATV(request):
    return render(request, 'Facturacion/FormularioATV.html')

from django.http import HttpResponse

def enviar_factura(request):
    return HttpResponse("Factura enviada.")


def Verificacioncomprobante(request):
    return render(request, 'Facturacion/Verificacioncomprobante.html')
