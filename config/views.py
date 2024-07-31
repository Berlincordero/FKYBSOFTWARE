from django.shortcuts import render

def index(request):
    return render(request, 'base.html')

def pos_view(request):
    return render(request, 'Terminal.html')

def producto_view(request):
    return render(request, 'producto.html')

def proforma_view(request):
    return render(request, 'proforma.html')


