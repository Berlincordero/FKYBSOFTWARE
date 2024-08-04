from django.shortcuts import render, redirect
from .forms import ConductorForm, PlacaDeVehiculoForm, RutaForm
from .models import Conductor, PlacaDeVehiculo, Ruta
from .forms import MiFormulario

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

def base2(request):
    return render(request, 'base2.html')

def modulo_transporte(request):
    # Datos de ejemplo
    conductores = [
        ('1', 'Conductor 1'),
        ('2', 'Conductor 2'),
    ]
    placas = [
        ('A123BC', 'A123BC'),
        ('B456CD', 'B456CD'),
    ]
    
    if request.method == 'POST':
        form_conductor = ConductorForm(request.POST)
        form_placa = PlacaDeVehiculoForm(request.POST)
        form_ruta = RutaForm(request.POST)
        
        if form_ruta.is_valid():
            # Aquí procesarías los datos del formulario
            return redirect('modulo_transporte')
    else:
        form_conductor = ConductorForm()
        form_placa = PlacaDeVehiculoForm()
        form_ruta = RutaForm()
    
    return render(request, 'modulo_transporte.html', {
        'form_conductor': form_conductor,
        'form_placa': form_placa,
        'form_ruta': form_ruta,
        'conductores': conductores,
        'placas': placas,
    })


def agregar_conductor(request):
    if request.method == 'POST':
        form = ConductorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agregar_conductor')
    else:
        form = ConductorForm()
    return render(request, 'modulo_transporte/agregar_conductor.html', {'form': form})

def agregar_placa(request):
    if request.method == 'POST':
        form = PlacaDeVehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agregar_placa')
    else:
        form = PlacaDeVehiculoForm()
    return render(request, 'modulo_transporte/agregar_placa.html', {'form': form})

def asignar_ruta(request):
    if request.method == 'POST':
        form = RutaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('asignar_ruta')
    else:
        form = RutaForm()
    return render(request, 'modulo_transporte/asignar_ruta.html', {'form': form})



def modulo_cliente(request):
    # Datos de ejemplo
    return render(request, 'modulo_cliente.html',{})