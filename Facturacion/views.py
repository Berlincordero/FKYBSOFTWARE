from django.shortcuts import render
from Cajaregistradora.models import Factura
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.timezone import now


def facturacion(request):
    facturas = Factura.objects.all()  # Obtener todas las facturas
    context = {"facturas": facturas}
    return render(request, 'Facturacion/facturacion.html', context)


def PrecierreCaja(request):
    return render(request, 'Facturacion/PrecierreCaja.html')







