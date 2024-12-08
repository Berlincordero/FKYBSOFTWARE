from django.conf import settings
from django.shortcuts import render
from .models import Factura
from datetime import datetime
from Inventario.models import Producto
from Orden_de_compra.models import OrdenDeCompra  # Importa el modelo de órdenes de compra
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Factura




def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    if ip == '127.0.0.1':
        ip = '192.168.0.101'  # Ajusta según tu entorno
    return ip

def Cajaregistradora_view(request):
    client_ip = get_client_ip(request)

    # Identificar sucursal y terminal según la IP
    sucursal = "Sucursal Desconocida"
    terminal = "Terminal Desconocida"
    for suc, terminales in settings.SUCURSAL_TERMINAL_CONFIG.items():
        for term, ip in terminales.items():
            if ip == client_ip:
                sucursal = suc
                terminal = term
                break

    # Cargar todos los productos activos
    productos = Producto.objects.filter(activo=True)

    # Cargar todas las órdenes de compra activas
    ordenes_compra = OrdenDeCompra.objects.filter(activo=True)

    # Generar la fecha y hora actual
    fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Formato: YYYY-MM-DD HH:MM:SS

    # Generar número de factura
    last_factura = Factura.objects.last()
    if last_factura:
        last_number = int(last_factura.numero_factura.split()[1])  # Obtiene el último número
    else:
        last_number = 0
    numero_factura = f"F {last_number + 1}"  # Genera el siguiente número

    # Agregar datos al contexto
    context = {
        'terminal': terminal,
        'sucursal': sucursal,
        'productos': productos,
        'ordenes_compra': ordenes_compra,  # Agregamos las órdenes de compra al contexto
        'fecha_hora_actual': fecha_hora_actual,
        'numero_factura': numero_factura,
    }

    return render(request, 'Cajaregistradora.html', context)



@csrf_exempt
def guardar_factura(request):
    if request.method == 'POST':
        try:
            datos = json.loads(request.body)
            productos = datos.get('productos', [])
            total_factura = 0
            for producto in productos:
                total_factura += float(producto['subtotal'])

            factura = Factura.objects.create(
                cliente=request.POST.get('cliente', 'Cliente Desconocido'),
                codigo=productos[0]['codigo'],
                nombre=productos[0]['nombre'],
                descripcion=productos[0]['descripcion'],
                cantidad=len(productos),
                precio_venta=total_factura,
                iva=total_factura * 0.13,
                total=total_factura * 1.13,
            )
            return JsonResponse({'status': 'success', 'message': 'Factura guardada exitosamente.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)