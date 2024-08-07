from django.shortcuts import render

# Create your views here.


def ventas(request):
    return render(request, 'Reportes/ventas.html')


def cuentasCobrar(request):
    return render(request, 'Reportes/cuentasCobrar.html')


def pagosFacturas(request):
    return render(request, 'Reportes/pagosFacturas.html')


def reporteUtilidades(request):
    return render(request, 'Reportes/reporteUtilidades.html')

def cierreCaja(request):
    return render(request, 'Reportes/cierreCaja.html')

def reporteProformas(request):
    return render(request, 'Reportes/reporteProformas.html')