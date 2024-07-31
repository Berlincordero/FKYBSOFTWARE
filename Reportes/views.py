from django.shortcuts import render

# Create your views here.


def ventas(request):
    return render(request, 'Reportes/ventas.html')


def cuentasCobrar(request):
    return render(request, 'Reportes/cuentasCobrar.html')


def pagosFacturas(request):
    return render(request, 'Reportes/pagosFacturas.html')