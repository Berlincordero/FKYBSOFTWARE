from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
from .models import Factura
from Inventario.models import Producto
from Orden_de_compra.models import OrdenDeCompra
from .models import Factura, AperturaCaja
from django.contrib import messages

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
    sucursal = "Sucursal Desconocida"
    terminal = "Terminal Desconocida"

    for suc, terminales in settings.SUCURSAL_TERMINAL_CONFIG.items():
        for term, ip in terminales.items():
            if ip == client_ip:
                sucursal = suc
                terminal = term
                break

    productos = Producto.objects.filter(activo=True)
    ordenes_compra = OrdenDeCompra.objects.filter(activo=True)
    fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    last_factura = Factura.objects.last()
    if last_factura:
        last_number = int(last_factura.numero_factura.split()[1])
    else:
        last_number = 0
    numero_factura = f"F {last_number + 1}"

    caja_abierta_mensaje = None
    caja_abierta_id = request.session.get('caja_abierta_id')
    apertura_fecha = None
    apertura_hora = None
    apertura_monto = None
    apertura_cajero = None  # Inicializamos la variable

    if caja_abierta_id:
        try:
            apertura = AperturaCaja.objects.get(id=caja_abierta_id)
            apertura_fecha = apertura.fecha_hora_apertura.strftime("%d/%m/%Y")
            apertura_hora = apertura.fecha_hora_apertura.strftime("%H:%M:%S")
            apertura_monto = apertura.monto_inicial
            apertura_cajero = apertura.cajero  # Obtenemos el cajero
            caja_abierta_mensaje = f"La caja la abrió {apertura_cajero} con un monto inicial de {apertura_monto}, a las {apertura_hora}."
        except AperturaCaja.DoesNotExist:
            del request.session['caja_abierta_id']

    context = {
        'terminal': terminal,
        'sucursal': sucursal,
        'productos': productos,
        'ordenes_compra': ordenes_compra,
        'fecha_hora_actual': fecha_hora_actual,
        'numero_factura': numero_factura,
        'caja_abierta_mensaje': caja_abierta_mensaje,
        'apertura_fecha': apertura_fecha,
        'apertura_hora': apertura_hora,
        'apertura_monto': apertura_monto,
        'apertura_cajero': apertura_cajero
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
                cliente=datos.get('cliente', 'Cliente Desconocido'),
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
        
        
def abrir_caja_view(request):
    if request.method == 'POST':
        cajero = request.POST.get('cajero')
        monto_inicial = request.POST.get('monto_inicial')

        # Guardar apertura en la base de datos
        apertura = AperturaCaja.objects.create(
            cajero=cajero,
            monto_inicial=monto_inicial
        )

        # Guardar el ID de la apertura en la sesión
        request.session['caja_abierta_id'] = apertura.id

        # Redirigir a la vista principal sin usar solo el messages de Django, 
        # ya que queremos persistencia en la recarga. 
        # Aun así puedes usar messages para el primer request si gustas.
        return redirect('Cajaregistradora_view')
    return render(request, 'Cajaregistradora.html')