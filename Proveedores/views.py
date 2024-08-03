from django.shortcuts import render


# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Proveedor
from .forms import ProveedorForm

"""
def proveedor_list(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedores/proveedor_list.html', {'proveedores': proveedores})

def proveedor_detail(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    return render(request, 'proveedores/proveedor_detail.html', {'proveedor': proveedor})

def proveedor_new(request):
    if request.method == "POST":
        form = ProveedorForm(request.POST)
        if form.is_valid():
            proveedor = form.save()
            return redirect('proveedor_list')
    else:
        form = ProveedorForm()
    return render(request, 'proveedores/proveedor_edit.html', {'form': form})

def proveedor_edit(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == "POST":
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            proveedor = form.save()
            return redirect('proveedor_list')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'proveedores/proveedor_edit.html', {'form': form})

def proveedor_delete(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('proveedor_list')
    return render(request, 'proveedores/proveedor_confirm_delete.html', {'proveedor': proveedor})

"""
def proveedor_list(request):
    return render(request, 'proveedores/proveedor_list.html')

def proveedor_detail(request):
    
    return render(request, 'proveedores/proveedor_detail.html')

def proveedor_new(request):
    form = ProveedorForm
    
    return render(request, 'proveedores/proveedor_edit.html',{'form': form})

def proveedor_edit(request):
    form = ProveedorForm
    
    return render(request, 'proveedores/proveedor_edit.html',{'form': form})

def proveedor_delete(request):
    
    return render(request, 'proveedores/proveedor_confirm_delete.html')