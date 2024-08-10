from django.shortcuts import render, redirect
from .models import Conductor, Vehiculo, Ruta
from django.http import JsonResponse

def modulo_transportes(request):
    return render(request, 'transportes/modulo_transportes.html')

def guardar_conductor(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido1 = request.POST.get('apellido1')
        apellido2 = request.POST.get('apellido2', '')
        cedula = request.POST.get('cedula')
        conductor = Conductor(nombre=nombre, apellido1=apellido1, apellido2=apellido2, cedula=cedula)
        conductor.save()
        return JsonResponse({'message': 'Conductor guardado correctamente'})

def guardar_vehiculo(request):
    if request.method == 'POST':
        numero_placa = request.POST.get('numero_placa')
        conductor_id = request.POST.get('conductor')
        conductor = Conductor.objects.get(id=conductor_id)
        vehiculo = Vehiculo(numero_placa=numero_placa, conductor=conductor)
        vehiculo.save()
        return JsonResponse({'message': 'Vehículo guardado correctamente'})

def guardar_ruta(request):
    if request.method == 'POST':
        numero_factura = request.POST.get('numero_factura')
        provincia = request.POST.get('provincia')
        canton = request.POST.get('canton')
        distrito = request.POST.get('distrito')
        direccion = request.POST.get('direccion')
        vehiculo_id = request.POST.get('vehiculo')
        vehiculo = Vehiculo.objects.get(id=vehiculo_id)
        ruta = Ruta(numero_factura=numero_factura, provincia=provincia, canton=canton, distrito=distrito, direccion=direccion, vehiculo=vehiculo)
        ruta.save()
        return JsonResponse({'message': 'Ruta guardada correctamente'})

def eliminar_todas_las_rutas(request):
    if request.method == 'POST':
        Ruta.objects.all().delete()
        return JsonResponse({'message': 'Todas las rutas han sido eliminadas'})

def imprimir_rutas(request):
    # Aquí puedes implementar la lógica para generar un PDF de las rutas
    return JsonResponse({'message': 'PDF de rutas generado'})
