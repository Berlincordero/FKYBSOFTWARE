
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Proveedor
from .forms import ProveedorForm




def proveedor_list(request):
    return render(request, 'proveedores/proveedor_list.html')
