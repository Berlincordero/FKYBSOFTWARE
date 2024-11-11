from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Cliente, ClienteEliminado
from .forms import ClienteForm
from django.db.models import Q
from django.utils import timezone

# Vista para mostrar todos los clientes
def modulo_clientes(request):
    # Filtrar solo los clientes activos
    clientes = Cliente.objects.filter(activo=True)  # Filtra solo clientes activos
    return render(request, 'clientes/modulo_clientes.html', {'clientes': clientes})
# Vista para buscar clientes por cédula, nombre o apellido
def buscar_clientes(request):
    query = request.GET.get('q', '')
    clientes = Cliente.objects.filter(
        Q(id_cliente__icontains=query) | 
        Q(nombre__icontains=query) | 
        Q(primer_apellido__icontains=query) | 
        Q(segundo_apellido__icontains=query)
    )
    return render(request, 'clientes/modulo_clientes.html', {'clientes': clientes, 'query': query})
# Vista para eliminar el cliente lógicamente
def eliminar_cliente(request, id_cliente):
    
    cliente = get_object_or_404(Cliente, id_cliente=id_cliente)
    ClienteEliminado.objects.create(
        cliente=cliente,
        fecha_eliminacion=timezone.now()
    )
    cliente.activo = False
    cliente.save()
    
    messages.success(request, f'Cliente {cliente.nombre} {cliente.primer_apellido} movido a eliminados con éxito.')
    
    # Redirigir al listado de clientes
    return redirect('clientes:modulo_clientes')
    
def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el cliente en la base de datos
            return redirect('clientes:modulo_clientes')  # Redirige a la lista de clientes
    else:
        form = ClienteForm()
    
    return render(request, 'clientes/agregar_cliente.html', {'form': form})
def editar_cliente(request, id_cliente):
    # Obtener el cliente a editar
    cliente = get_object_or_404(Cliente, id_cliente=id_cliente)
    
    # Si el formulario se envía por POST
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()  # Guarda los cambios en el cliente
            return redirect('clientes:modulo_clientes')  # Redirige a la lista de clientes
    else:
        # Si es GET, inicializamos el formulario con los datos del cliente
        form = ClienteForm(instance=cliente)
    
    return render(request, 'clientes/editar_cliente.html', {'form': form, 'cliente': cliente})