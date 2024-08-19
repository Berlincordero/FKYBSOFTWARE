from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import OrdenDeCompra
from .forms import OrdenDeCompraForm

def orden_de_compra(request):
    return render(request, 'ordenes/orden_de_compra.html')
