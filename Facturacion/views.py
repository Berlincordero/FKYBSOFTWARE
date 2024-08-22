from django.shortcuts import render

def facturacion_view(request):
    return render(request, 'facturacion.html')
