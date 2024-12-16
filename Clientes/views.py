#Clientes/views
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Cliente, ClienteEliminado
from .forms import ClienteForm
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse
from .models import Cliente  # Asegúrate de que el modelo Cliente esté bien definido



# Vista para mostrar todos los clientes
def modulo_clientes(request):
    # Filtrar solo los clientes activos
    clientes = Cliente.objects.filter(activo=True)  # Filtra solo clientes activos
    return render(request, 'clientes/modulo_clientes.html', {'clientes': clientes})
# Vista para buscar clientes por cédula, nombre o apellido




    
def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el cliente en la base de datos
            return redirect('clientes:modulo_clientes')  # Redirige a la lista de clientes
    else:
        form = ClienteForm()
    
    return render(request, 'clientes/agregar_cliente.html', {'form': form})

def eliminar_cliente(request, id_cliente):
    if request.method == 'POST':
        try:
            # Obtiene el cliente que deseas "eliminar"
            cliente = get_object_or_404(Cliente, id_cliente=id_cliente)
            
            # Mueve el cliente a ClienteEliminado (si aplica)
            ClienteEliminado.objects.create(
                cliente=cliente, 
                fecha_eliminacion=timezone.now()
            )
            
            # Marca el cliente como inactivo
            cliente.activo = False
            cliente.save()

            messages.success(request, 'Cliente eliminado con éxito.')
        except Exception as e:
            # Si ocurre un error, muestra un mensaje
            messages.error(request, f'Error al eliminar el cliente: {str(e)}')

        return redirect('clientes:modulo_clientes')


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


#--------------------parte de caja registradora para exportar clientes---------------------
#---------------------hecho por Berlín---------------------

def buscar_clientes(request):
    if request.method == "GET":
        query = request.GET.get('q', '').strip()  # Obtener el término de búsqueda

        # Validar si el término de búsqueda está vacío
        if not query:
            return JsonResponse([], safe=False)

        print(f"Término de búsqueda: {query}")  # Depuración

        # Buscar coincidencias en nombre, primer apellido y segundo apellido
        clientes = Cliente.objects.filter(
            Q(nombre__icontains=query) | 
            Q(primer_apellido__icontains=query) | 
            Q(segundo_apellido__icontains=query)
        )

        print(f"Resultados encontrados: {[f'{c.nombre} {c.primer_apellido} {c.segundo_apellido}' for c in clientes]}")  # Depuración

        # Serializar los resultados
        resultados = [
            {
                "id": cliente.id_cliente,
                "nombre": cliente.nombre,
                "primer_apellido": cliente.primer_apellido,
                "segundo_apellido": cliente.segundo_apellido
            }
            for cliente in clientes
        ]

        return JsonResponse(resultados, safe=False)