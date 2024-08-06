from django.shortcuts import render, redirect
from .forms import ConductorForm, PlacaDeVehiculoForm, RutaForm

def index(request):
    return render(request, 'base.html')

def pos_view(request):
    return render(request, 'Terminal.html')

def producto_view(request):
    return render(request, 'producto.html')

def proforma_view(request):
    return render(request, 'proforma.html')

def facturacion_view(request):
    return render(request, 'facturacion.html')

def informacion_view(request):
    return render(request, 'informacion.html')



def modulo_transporte(request):
    form_conductor = ConductorForm()
    form_placa = PlacaDeVehiculoForm()
    form_ruta = RutaForm()

    return render(request, 'modulo_transporte.html', {
        'form_conductor': form_conductor,
        'form_placa': form_placa,
        'form_ruta': form_ruta
    })

def agregar_conductor(request):
    
    
    form = ConductorForm()
    return render(request, 'modulo_transporte/agregar_conductor.html', {'form': form})

def agregar_placa(request):
    
    form = PlacaDeVehiculoForm()
    return render(request, 'modulo_transporte/agregar_placa.html', {'form': form})

def asignar_ruta(request):
    
    form = RutaForm()
    return render(request, 'modulo_transporte/asignar_ruta.html', {'form': form})



def modulo_cliente(request):
    # Datos de ejemplo
    return render(request, 'modulo_cliente.html',{})