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
from .models import MovimientoDinero
from django.db.models import Sum
from django.http import HttpResponse
from .models import PreCierre


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
    apertura_cajero = None

    if caja_abierta_id:
        try:
            apertura = AperturaCaja.objects.get(id=caja_abierta_id)
            apertura_fecha = apertura.fecha_hora_apertura.strftime("%d/%m/%Y")
            apertura_hora = apertura.fecha_hora_apertura.strftime("%H:%M:%S")
            apertura_monto = apertura.monto_inicial
            apertura_cajero = apertura.cajero
            caja_abierta_mensaje = f"La caja la abrió {apertura_cajero} con un monto inicial de {apertura_monto}, a las {apertura_hora}."
        except AperturaCaja.DoesNotExist:
            del request.session['caja_abierta_id']
    
    # Aquí obtenemos todos los movimientos para mostrarlos en la tabla de precierre
    movimientos = MovimientoDinero.objects.all().order_by('-fecha_hora')  # ordenados por fecha desc, si se desea
    total_movimientos = movimientos.aggregate(total=Sum('monto'))['total'] or 0

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
        'apertura_cajero': apertura_cajero,
        'movimientos': movimientos,  # Agregamos movimientos al contexto
        'total_movimientos': total_movimientos,  # El total sumado de todos los movimientos
    
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

def guardar_movimiento_dinero(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipoMovimiento')
        fecha_hora = request.POST.get('fechaHora')
        usuario = request.POST.get('usuario')
        nota = request.POST.get('nota')
        monto = request.POST.get('monto')

        # Convertir fecha_hora al objeto datetime (si necesario)
        # fecha_hora viene en formato "YYYY-MM-DDTHH:MM", por ejemplo: "2024-12-11T15:30"
        # Se puede convertir con:
        fecha_hora_dt = datetime.strptime(fecha_hora, "%Y-%m-%dT%H:%M")

        # Crear el movimiento en la base de datos
        MovimientoDinero.objects.create(
            tipo_movimiento=tipo,
            fecha_hora=fecha_hora_dt,
            usuario=usuario,
            nota=nota,
            monto=monto
        )

        # Redirigir a la vista principal que muestra el precierre
        return redirect('Cajaregistradora_view')
    else:
        # Si no es POST, simplemente redirige a la vista principal
        return redirect('Cajaregistradora_view')
    
    
@csrf_exempt
def guardar_precierre(request):
    if request.method == 'POST':
        try:
            # Parsear los datos enviados en la solicitud
            datos = json.loads(request.body)
            print("Datos recibidos para PreCierre:", datos)  # Para depuración

            # Obtener y validar la fecha
            fecha_str = datos.get('fecha')
            if not fecha_str:
                return JsonResponse({'success': False, 'error': 'La fecha de apertura es requerida.'}, status=400)
            try:
                fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Formato de fecha inválido. Debe ser YYYY-MM-DD.'}, status=400)

            # Obtener y validar la hora apertura
            hora_apertura_str = datos.get('hora_apertura')
            if hora_apertura_str and hora_apertura_str != "No disponible":
                try:
                    hora_apertura_obj = datetime.strptime(hora_apertura_str, '%H:%M:%S').time()
                except ValueError:
                    return JsonResponse({'success': False, 'error': 'Formato de hora inválido. Debe ser HH:MM:SS.'}, status=400)
            else:
                hora_apertura_obj = None

            # Crear el registro del precierre en la base de datos
            precierre = PreCierre.objects.create(
                sucursal=datos.get('sucursal', 'Desconocida'),
                caja_registradora=datos.get('caja_registradora', 'Desconocida'),
                hora_apertura=hora_apertura_obj,
                fecha=fecha_obj,
                monto_inicial=datos.get('monto_inicial', 0.00),
                cajero=datos.get('cajero', 'No disponible'),
                impuestos=datos.get('impuestos', 0.00),
                efectivo=datos.get('efectivo', 0.00),
                facturas_proveedor=datos.get('facturas_proveedor', 0),
                tarjetas=datos.get('tarjetas', 0.00),
                simpe_movil=datos.get('simpe_movil', 0.00),
                venta_credito=datos.get('venta_credito', 0.00),
                movimientos=datos.get('movimientos', 0.00),
                total_ventas=datos.get('total_ventas', 0.00),
                cantidad_facturas=datos.get('cantidad_facturas', 0),
                conteo_efectivo=datos.get('conteo_efectivo', 0.00),
                conteo_tarjetas=datos.get('conteo_tarjetas', 0.00),
                contado_efectivo=datos.get('contado_efectivo', 0.00),
                contado_tarjetas=datos.get('contado_tarjetas', 0.00),
            )

            # Retornar una respuesta exitosa en formato JSON
            return JsonResponse({'success': True, 'message': 'Precierre guardado con éxito.'})
        except Exception as e:
            # Retornar una respuesta de error en formato JSON
            print(f"Error al guardar PreCierre: {e}")  # Para depuración
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    # Si el método no es POST, retornar un error
    return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)