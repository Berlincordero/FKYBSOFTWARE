#transportes/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Conductor, ConductorEliminado, Vehiculo, Ruta, RutaEliminada, VehiculoEliminado
from .forms import ConductorForm, VehiculoForm, RutaForm
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView
from django.utils import timezone
import datetime
from django.contrib import messages
from geografia.models import Provincia, Canton, Distrito

@login_required
def modulo_transportes(request):
    conductores = Conductor.objects.filter(activo=True)  # Obtener todos los conductores en activos
    vehiculos = Vehiculo.objects.all()  # Obtener todos los vehículos
    return render(request, 'modulo_transportes.html', {'conductores': conductores, 'vehiculos': vehiculos})


class ConductorListView(ListView):
    model = Conductor
    template_name = 'modulo_transportes.html'  # Nombre de tu plantilla
    context_object_name = 'conductores'  # Nombre que usaremos en la plantilla
@login_required
def agregar_conductor(request):
    if request.method == 'POST':
        id_conductor = request.POST.get('id_conductor')
        nombre_conductor = request.POST.get('nombre_conductor')
        apellidos_1 = request.POST.get('apellidos_1')
        apellidos_2 = request.POST.get('apellidos_2')

        try:
            nuevo_conductor = Conductor(
                id_conductor=id_conductor,
                nombre_conductor=nombre_conductor,
                apellidos_1=apellidos_1,
                apellidos_2=apellidos_2
            )
            nuevo_conductor.save()
            return redirect('modulo_transportes')
        except Exception as e:
            print(f"Error: {e}")  # Muestra el error en la consola
            return HttpResponse("Error al agregar conductor: " + str(e), status=500)

    return render(request, 'modulo_transportes.html')

def editar_conductor(request, id_conductor):
    conductor = get_object_or_404(Conductor, id_conductor=id_conductor)
    
    if request.method == 'POST':
        conductor.nombre_conductor = request.POST['nombre_conductor']
        conductor.apellidos_1 = request.POST['apellidos_1']
        conductor.apellidos_2 = request.POST['apellidos_2']
        conductor.save()
        return redirect('transportes:modulo_transportes')
    
    return render(request, 'modulo_transportes.html', {'conductor': conductor})





@login_required
def eliminar_conductor(request, id_conductor):
    if request.method == 'POST':
        conductor = get_object_or_404(Conductor, id_conductor=id_conductor)
        ConductorEliminado.objects.create(
            conductor=conductor,
            fecha_eliminacion=timezone.now()
        )
        conductor.activo = False
        conductor.save()

        messages.success(request, 'Conductor movido a eliminadas con éxito.')
        return redirect('modulo_transportes')
    return HttpResponse("Método no permitido", status=405)




#                VEHICULOS   
@login_required
def modulo_vehiculos(request):
    vehiculos = Vehiculo.objects.filter(activo=True)  # Obtener todos los vehículos
    return render(request, 'modulo_vehiculos.html', {'vehiculos': vehiculos})
@login_required
def agregar_vehiculo(request):
    if request.method == 'POST':
        id_vehiculo = request.POST['id_vehiculo']  # Toma el número de placa ingresado
        marca = request.POST['marca']
        modelo = request.POST['modelo']
        año = request.POST['año']
        
        # Guarda el nuevo vehículo
        Vehiculo.objects.create(id_vehiculo=id_vehiculo, marca=marca, modelo=modelo, año=año)
        return redirect('transportes:modulo_vehiculos')  # Redirige a la lista de vehículos
    
    return render(request, 'modulo_vehiculos.html')


@login_required
def editar_vehiculo(request, id_vehiculo):
    vehiculo = get_object_or_404(Vehiculo, id_vehiculo=id_vehiculo)
    
    if request.method == 'POST':
        vehiculo.marca = request.POST['marca']
        vehiculo.modelo = request.POST['modelo']
        vehiculo.año = request.POST['año']
        vehiculo.save()
        return redirect('transportes:modulo_vehiculos')
    
    return render(request, 'modulo_vehiculos.html', {'vehiculo': vehiculo})


@login_required
def eliminar_vehiculo(request, id_vehiculo):
    if request.method == 'POST':
        vehiculo = get_object_or_404(Vehiculo, id_vehiculo=id_vehiculo)
        VehiculoEliminado.objects.create(
            vehiculo=vehiculo,
            fecha_eliminacion=timezone.now()
        )
        vehiculo.activo = False
        vehiculo.save()

        messages.success(request, 'Vehiculo movido a eliminadas con éxito.')
        return redirect('transportes:modulo_vehiculos')
    return HttpResponse("Método no permitido", status=405)




# Rutas #

#transportes/views.py
@login_required
def modulo_rutas(request):
    # Si estás usando un campo 'activo' en el modelo Ruta
    rutas = Ruta.objects.filter(activo=True)  # Recupera todas las rutas sin filtrar  # Filtra por rutas activas
    conductores = Conductor.objects.all()
    vehiculos = Vehiculo.objects.all()
    return render(request, 'modulo_rutas.html', {'rutas': rutas, 'conductores': conductores, 'vehiculos': vehiculos})





@login_required
def agregar_ruta(request):
    if request.method == 'POST':
        id_ruta = request.POST.get('id_ruta')
        fecha_ruta = request.POST.get('fecha_ruta')
        provincia = request.POST.get('provincia')
        canton = request.POST.get('canton')
        distrito = request.POST.get('distrito')
        direccion_exacta = request.POST.get('direccion_exacta')
        nombre_conductor_id = request.POST.get('nombre_conductor')  # ID del conductor
        id_vehiculo_id = request.POST.get('id_vehiculo')  # ID del vehículo

        # Obtener instancias de Conductor y Vehículo
        conductor = get_object_or_404(Conductor, id_conductor=nombre_conductor_id)
        vehiculo = get_object_or_404(Vehiculo, id_vehiculo=id_vehiculo_id)

        nueva_ruta = Ruta(
            id_ruta=id_ruta,
            fecha_ruta=fecha_ruta,
            provincia=provincia,
            canton=canton,
            distrito=distrito,
            direccion_exacta=direccion_exacta,
            nombre_conductor=conductor,  # Asigna la instancia de Conductor
            id_vehiculo=vehiculo  # Asigna la instancia de Vehículo
        )
        nueva_ruta.save()
        messages.success(request, 'Ruta agregada exitosamente.')
        return redirect('transportes:modulo_rutas')
    else:
        return redirect('transportes:modulo_rutas')

@login_required
def eliminar_ruta(request, id):
    if request.method == 'POST':
        # Obtiene la ruta que quieres "eliminar"
        ruta = get_object_or_404(Ruta, id_ruta=id)
        
        # Si ya tienes una tabla RutaEliminada, mueve la ruta allí
        RutaEliminada.objects.create(
            ruta=ruta,  # Asume que RutaEliminada tiene un campo 'ruta' que guarda la ruta original
            fecha_eliminacion=timezone.now()
        )
        
        # Marca la ruta como inactiva en lugar de eliminarla (opcional, dependiendo de tu modelo)
        ruta.activo = False  # Suponiendo que tienes un campo 'activo' para marcar como inactiva
        ruta.save()

        messages.success(request, 'Ruta movida a eliminadas con éxito.')
        return redirect('transportes:modulo_rutas')




    
@login_required    
def editar_ruta(request, id_ruta):
    ruta = get_object_or_404(Ruta, id_ruta=id_ruta)
    
    if request.method == 'POST':
        ruta.fecha_ruta = request.POST['fecha_ruta']
        ruta.provincia = request.POST['provincia']
        ruta.canton = request.POST['canton']
        ruta.distrito = request.POST['distrito']
        ruta.direccion_exacta = request.POST['direccion_exacta']
        
        # Obtener los objetos de Conductor y Vehículo
        nombre_conductor = get_object_or_404(Conductor, id_conductor=request.POST['nombre_conductor'])
        id_vehiculo = get_object_or_404(Vehiculo, id_vehiculo=request.POST['id_vehiculo'])
        
        ruta.nombre_conductor = nombre_conductor
        ruta.id_vehiculo = id_vehiculo
        ruta.save()

        messages.success(request, 'Ruta actualizada con éxito.')
        return redirect('transportes:modulo_rutas')

    return render(request, 'modulo_rutas.html', {'ruta': ruta})

@login_required
def asignar_rutas(request):
    # Obtener todas las provincias
    provincias = Provincia.objects.all()  
    return render(request, 'modulo_rutas.html', {'provincias': provincias})
@login_required
def eliminar_todas_rutas(request):
    if request.method == 'POST':
        Ruta.objects.all().delete()  # Elimina todas las rutas
        return redirect('transportes:asignar_rutas')  # Redirigir a la página de asignar rutas
    



