#transportes/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Conductor, ConductorEliminado, Vehiculo, Ruta, RutaEliminada
from .forms import ConductorForm, VehiculoForm, RutaForm
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView
from django.utils import timezone
import datetime
from django.contrib import messages


def modulo_transportes(request):
    conductores = Conductor.objects.all()  # Obtener todos los conductores
    vehiculos = Vehiculo.objects.all()  # Obtener todos los vehículos
    return render(request, 'modulo_transportes.html', {'conductores': conductores, 'vehiculos': vehiculos})


class ConductorListView(ListView):
    model = Conductor
    template_name = 'modulo_transportes.html'  # Nombre de tu plantilla
    context_object_name = 'conductores'  # Nombre que usaremos en la plantilla

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
        form = ConductorForm(request.POST, instance=conductor)
        if form.is_valid():
            form.save()
            return redirect('modulo_transportes')  # Redirigir a la lista de conductores
    else:
        form = ConductorForm(instance=conductor)

    return render(request, 'editar_conductor.html', {'form': form})






def eliminar_conductor(request, id_conductor):
    conductor = get_object_or_404(Conductor, id_conductor=id_conductor)

    if request.method == 'POST':
        # Guardar el conductor en la tabla de eliminados
        ConductorEliminado.objects.create(conductor=conductor)
        # Eliminar el conductor original
        conductor.delete()
        return redirect('modulo_transportes')  # Redirigir después de eliminar

    # Mostrar modal de confirmación si no es un POST
    return render(request, 'modulo_transportes.html', {'conductores': Conductor.objects.all()})



#                VEHICULOS   

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



def editar_vehiculo(request, id_vehiculo):
    vehiculo = get_object_or_404(Vehiculo, id_vehiculo=id_vehiculo)
    
    if request.method == 'POST':
        vehiculo.marca = request.POST['marca']
        vehiculo.modelo = request.POST['modelo']
        vehiculo.año = request.POST['año']
        vehiculo.save()
        return redirect('transportes:modulo_vehiculos')
    
    return render(request, 'modulo_vehiculos.html', {'vehiculo': vehiculo})



def eliminar_vehiculo(request, id_vehiculo):
    vehiculo = get_object_or_404(Vehiculo, id_vehiculo=id_vehiculo)
    
    if request.method == 'POST':
        vehiculo.delete()  # Eliminar el vehículo
        return redirect('transportes:modulo_vehiculos')  # Redirigir a la lista de vehículos




def modulo_vehiculos(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'modulo_vehiculos.html', {'vehiculos': vehiculos})




# Rutas #

#transportes/views.py

def modulo_rutas(request):
    rutas = Ruta.objects.all()  # Asegúrate de que Ruta es tu modelo de rutas
    conductores = Conductor.objects.all()
    vehiculos = Vehiculo.objects.all()
    return render(request, 'modulo_rutas.html', {'rutas': rutas, 'conductores': conductores, 'vehiculos': vehiculos})




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


def eliminar_ruta(request, id):
    if request.method == 'POST':
        # Cambia 'id' por 'id_ruta' si estás utilizando 'id_ruta' en tu modelo Ruta
        ruta = get_object_or_404(Ruta, id_ruta=id)  
        
        # Crea un nuevo registro en RutaEliminada antes de eliminar
        RutaEliminada.objects.create(
            ruta=ruta,  # Esto asume que tienes un ForeignKey llamado 'ruta' en RutaEliminada
            fecha_eliminacion=timezone.now(),
            # Aquí puedes agregar más campos si es necesario
        )

        # Elimina la ruta
        ruta.delete()
        messages.success(request, 'Ruta eliminada con éxito.')
        
        # Redirige a la vista deseada
        return redirect('transportes:modulo_rutas')


    
    
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


def asignar_rutas(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        fecha_ruta = request.POST.get('fecha_ruta')
        provincia = request.POST.get('provincia')
        canton = request.POST.get('canton')
        distrito = request.POST.get('distrito')
        direccion_exacta = request.POST.get('direccion_exacta')
        nombre_conductor = request.POST.get('nombre_conductor')
        id_vehiculo = request.POST.get('id_vehiculo')

        # Crear una nueva ruta
        try:
            nueva_ruta = Ruta(
                fecha_ruta=fecha_ruta,
                provincia=provincia,
                canton=canton,
                distrito=distrito,
                direccion_exacta=direccion_exacta,
                nombre_conductor=nombre_conductor,
                id_vehiculo=id_vehiculo
            )
            nueva_ruta.save()
            messages.success(request, 'Ruta asignada exitosamente.')
            return redirect('transportes:asignar_rutas')  # Redirigir a la misma página después de guardar
        except Exception as e:
            messages.error(request, f'Error al asignar ruta: {str(e)}')

    # Obtener todas las rutas para mostrarlas en el template
    rutas = Ruta.objects.all()
    return render(request, 'asignar_rutas.html', {'rutas': rutas})

def eliminar_todas_rutas(request):
    if request.method == 'POST':
        Ruta.objects.all().delete()  # Elimina todas las rutas
        return redirect('transportes:asignar_rutas')  # Redirigir a la página de asignar rutas