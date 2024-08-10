from django.shortcuts import render, redirect

def index(request):
    return render(request, 'base.html')

def pos_view(request):
    return render(request, 'terminal.html')

def producto_view(request):
    return render(request, 'producto.html')

def proforma_view(request):
    return render(request, 'proforma.html')

def facturacion_view(request):
    return render(request, 'facturacion.html')

def informacion_view(request):
    return render(request, 'informacion.html')

def modulo_transportes(request):
    return render(request, 'modulo_transportes.html')

def modulo_cliente(request):
    # Datos de ejemplo
    return render(request, 'modulo_cliente.html',{})