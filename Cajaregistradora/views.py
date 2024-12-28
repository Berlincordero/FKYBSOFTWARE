from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
from decimal import Decimal
from .models import Factura, AperturaCaja, MovimientoDinero, PreCierre
from Inventario.models import Producto
from Orden_de_compra.models import OrdenDeCompra
from django.db.models import Sum
from django.utils import timezone
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
        for term, ip_dir in terminales.items():
            if ip_dir == client_ip:
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
    fecha_hora_cierre = None  # Nuevo

    if caja_abierta_id:
        try:
            apertura = AperturaCaja.objects.get(id=caja_abierta_id)
            apertura_fecha = apertura.fecha_hora_apertura.strftime("%d/%m/%Y")
            apertura_hora = apertura.fecha_hora_apertura.strftime("%H:%M:%S")
            apertura_monto = apertura.monto_inicial
            apertura_cajero = apertura.cajero
            caja_abierta_mensaje = f"La caja la abrió {apertura_cajero} con un monto inicial de {apertura_monto}, a las {apertura_hora}."
            fecha_hora_cierre = apertura.fecha_hora_cierre.strftime("%d/%m/%Y %H:%M:%S") if apertura.fecha_hora_cierre else None
        except AperturaCaja.DoesNotExist:
            del request.session['caja_abierta_id']

    # Obtener todos los movimientos (monto es DecimalField, sum retorna Decimal)
    movimientos = MovimientoDinero.objects.all().order_by('-fecha_hora')
    total_movimientos = movimientos.aggregate(total=Sum('monto'))['total'] or Decimal('0.00')

    # Inicializar acumulados como Decimal
    impuestos_acumulados = Decimal('0.00')
    efectivo_acumulado = Decimal('0.00')
    facturas_proveedor_acumulado = Decimal('0.00')
    tarjetas_acumulado = Decimal('0.00')
    simpe_movil_acumulado = Decimal('0.00')
    venta_credito_acumulado = Decimal('0.00')
    total_ventas = Decimal('0.00')
    conteo_efectivo = Decimal('0.00')
    cantidad_facturas = 0

    if caja_abierta_id:
        # Obtenemos la fecha-hora de apertura
        apertura = AperturaCaja.objects.get(id=caja_abierta_id)
        apertura_dt = apertura.fecha_hora_apertura

        # Facturas desde la apertura (fecha es DateTimeField, se compara con datetime)
        facturas_desde_apertura = Factura.objects.filter(fecha__gte=apertura_dt)

        # IVA acumulado
        impuestos_acumulados = facturas_desde_apertura.aggregate(total_iva=Sum('iva'))['total_iva'] or Decimal('0.00')

        # Sumar métodos de pago
        for f in facturas_desde_apertura:
            # f.total es Decimal
            if f.metodo_pago == 'cash':
                efectivo_acumulado += f.total
            elif f.metodo_pago == 'creditCard':
                tarjetas_acumulado += f.total
            elif f.metodo_pago == 'simpeMovil':
                simpe_movil_acumulado += f.total
            elif f.metodo_pago == 'credit':
                venta_credito_acumulado += f.total
            # transfer no se suma a ninguno

            if f.tipo_precio.lower() == 'proveedor':
                facturas_proveedor_acumulado += f.total

        # Cantidad de facturas
        cantidad_facturas = facturas_desde_apertura.count()

        # Total de ventas = (Efectivo + Tarjetas + Simpe + Credito) - Facturas Proveedor
        total_ventas = (efectivo_acumulado + tarjetas_acumulado + simpe_movil_acumulado + venta_credito_acumulado) - facturas_proveedor_acumulado

        # Conteo efectivo = Efectivo Acumulado - Movimientos - Facturas Proveedor
        # Todas las variables son Decimal, así que no hay problema de tipos
        conteo_efectivo = efectivo_acumulado - total_movimientos - facturas_proveedor_acumulado - venta_credito_acumulado

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
        'fecha_hora_cierre': fecha_hora_cierre,  # Añadido
        'movimientos': movimientos,
        'total_movimientos': total_movimientos,

        'impuestos_acumulados': impuestos_acumulados,
        'efectivo_acumulado': efectivo_acumulado,
        'facturas_proveedor_acumulado': facturas_proveedor_acumulado,
        'tarjetas_acumulado': tarjetas_acumulado,
        'simpe_movil_acumulado': simpe_movil_acumulado,
        'venta_credito_acumulado': venta_credito_acumulado,

        'total_ventas': total_ventas,
        'cantidad_facturas': cantidad_facturas,
        'conteo_efectivo': conteo_efectivo,
    }

    return render(request, 'Cajaregistradora.html', context)




@csrf_exempt
def guardar_factura(request):
    if request.method == 'POST':
        try:
            datos = json.loads(request.body)
            productos = datos.get('productos', [])
            total_factura = Decimal('0.00')

            for producto in productos:
                subtotal = Decimal(str(producto['subtotal']))
                total_factura += subtotal

            iva = total_factura * Decimal('0.13')
            total_con_iva = total_factura + iva

            tipo_precio = datos.get('tipo_precio', 'Regular')
            metodo_pago = datos.get('metodo_pago', 'cash')

            # Obtener la caja abierta desde la sesión
            caja_abierta_id = request.session.get('caja_abierta_id')
            apertura_caja = AperturaCaja.objects.get(id=caja_abierta_id, abierta=True) if caja_abierta_id else None

            factura = Factura.objects.create(
                apertura_caja=apertura_caja,
                cliente=datos.get('cliente', 'Cliente Desconocido'),
                codigo=productos[0]['codigo'] if productos else '',
                nombre=productos[0]['nombre'] if productos else '',
                descripcion=productos[0]['descripcion'] if productos else '',
                cantidad=len(productos),
                precio_venta=total_factura,
                iva=iva,
                total=total_con_iva,
                tipo_precio=tipo_precio,
                metodo_pago=metodo_pago
            )

            return JsonResponse({'success': True, 'message': 'Factura guardada exitosamente.'})
        except AperturaCaja.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'No hay una caja abierta.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)
    


def abrir_caja_view(request):
    if request.method == 'POST':
        cajero = request.POST.get('cajero')
        monto_inicial_str = request.POST.get('monto_inicial', '0.00')
        codigo_seguridad = request.POST.get('codigo_seguridad')  # Obtener el código de seguridad
        monto_inicial = Decimal(monto_inicial_str)

        # Validar el código de seguridad
        codigo_correcto = "KIK301"  # Reemplaza esto con el código real o lógica de validación
        if codigo_seguridad != codigo_correcto:
            # Si el código es incorrecto, añadir un mensaje de error
            messages.error(request, 'Código de seguridad incorrecto. No se puede abrir la caja.')
            return redirect('Cajaregistradora_view')

        # Verificar si ya hay una caja abierta
        if AperturaCaja.objects.filter(abierta=True).exists():
            messages.error(request, 'Ya hay una caja abierta.')
            return redirect('Cajaregistradora_view')

        # Crear una nueva apertura de caja
        apertura = AperturaCaja.objects.create(
            cajero=cajero,
            monto_inicial=monto_inicial,
            codigo_seguridad=codigo_seguridad  # Guardar el código de seguridad
        )

        # Guardar el ID de la caja abierta en la sesión
        request.session['caja_abierta_id'] = apertura.id

        # Añadir un mensaje de éxito
        messages.success(request, 'Caja abierta exitosamente.')
        return redirect('Cajaregistradora_view')
    
    # Si no es POST, simplemente redirigir a la vista principal
    return redirect('Cajaregistradora_view')




def guardar_movimiento_dinero(request):
    if request.method == 'POST':
        try:
            # Obtener datos desde el formulario
            tipo = request.POST.get('tipoMovimiento')
            fecha_hora_str = request.POST.get('fechaHora')
            usuario = request.POST.get('usuario')
            nota = request.POST.get('nota', '')
            monto_str = request.POST.get('monto', '0.00')
            monto = Decimal(monto_str)
            codigo_seguridad = request.POST.get('codigo_seguridad')  # Obtener la clave de seguridad

            # Validar el código de seguridad
            codigo_correcto = "KIK301"  # Cambia esto a la clave que deseas validar
            if codigo_seguridad != codigo_correcto:
                # Si la clave es incorrecta, mostrar mensaje de error y detener la operación
                messages.error(request, 'Código de seguridad incorrecto. No se puede realizar el movimiento.')
                return redirect('Cajaregistradora_view')

            # Convertir la fecha y hora al formato datetime
            fecha_hora_dt = datetime.strptime(fecha_hora_str, "%Y-%m-%dT%H:%M")

            # Obtener la caja abierta desde la sesión
            caja_abierta_id = request.session.get('caja_abierta_id')
            if not caja_abierta_id:
                messages.error(request, 'No hay una caja abierta.')
                return redirect('Cajaregistradora_view')

            apertura_caja = AperturaCaja.objects.get(id=caja_abierta_id, abierta=True)

            # Crear el movimiento de dinero
            MovimientoDinero.objects.create(
                apertura_caja=apertura_caja,
                tipo_movimiento=tipo,
                fecha_hora=fecha_hora_dt,
                usuario=usuario,
                nota=nota,
                monto=monto
            )

            # Mostrar mensaje de éxito y redirigir
            messages.success(request, 'Movimiento de dinero registrado con éxito.')
            return redirect('Cajaregistradora_view')

        except AperturaCaja.DoesNotExist:
            messages.error(request, 'No se encontró la caja abierta.')
            return redirect('Cajaregistradora_view')

        except Exception as e:
            # Registrar un mensaje de error genérico
            messages.error(request, f'Ocurrió un error: {str(e)}')
            return redirect('Cajaregistradora_view')

    else:
        messages.error(request, 'Método no permitido.')
        return redirect('Cajaregistradora_view')

@csrf_exempt
def guardar_precierre(request):
    if request.method == 'POST':
        try:
            # Obtener el ID de la caja abierta desde la sesión
            caja_abierta_id = request.session.get('caja_abierta_id')
            if not caja_abierta_id:
                return JsonResponse({'success': False, 'message': 'No hay una caja abierta.'}, status=400)

            apertura = AperturaCaja.objects.get(id=caja_abierta_id, abierta=True)

            datos = json.loads(request.body)

            # Obtener el código de seguridad desde los datos enviados
            codigo_seguridad = datos.get('codigo_seguridad')

            # Validar el código de seguridad
            codigo_correcto = "KIK301"  # Reemplaza esto con tu lógica de validación real
            if codigo_seguridad != codigo_correcto:
                return JsonResponse({'success': False, 'message': 'Código de seguridad incorrecto.'}, status=403)

            # Crear el objeto PreCierre vinculado a AperturaCaja
            precierre = PreCierre.objects.create(
                apertura_caja=apertura,
                sucursal=datos.get('sucursal', 'Desconocida'),
                caja_registradora=datos.get('caja_registradora', 'Desconocida'),
                hora_apertura=apertura.fecha_hora_apertura.time() if apertura.fecha_hora_apertura else None,
                fecha=apertura.fecha_hora_apertura.date() if apertura.fecha_hora_apertura else None,
                monto_inicial=Decimal(datos.get('monto_inicial', '0.00')),
                cajero=datos.get('cajero', apertura.cajero),
                impuestos=Decimal(datos.get('impuestos', '0.00')),
                efectivo=Decimal(datos.get('efectivo', '0.00')),
                facturas_proveedor=int(datos.get('facturas_proveedor', 0)),
                tarjetas=Decimal(datos.get('tarjetas', '0.00')),
                simpe_movil=Decimal(datos.get('simpe_movil', '0.00')),
                venta_credito=Decimal(datos.get('venta_credito', '0.00')),
                movimientos=Decimal(datos.get('movimientos', '0.00')),
                total_ventas=Decimal(datos.get('total_ventas', '0.00')),
                cantidad_facturas=int(datos.get('cantidad_facturas', 0)),
                conteo_efectivo=Decimal(datos.get('conteo_efectivo', '0.00')),
                conteo_tarjetas=Decimal(datos.get('conteo_tarjetas', '0.00')),
                contado_efectivo=Decimal(datos.get('contado_efectivo', '0.00')),
                contado_tarjetas=Decimal(datos.get('contado_tarjetas', '0.00')),
            )

            # Marcar la caja como cerrada y guardar la hora de cierre
            apertura.abierta = False
            apertura.fecha_hora_cierre = timezone.now()
            apertura.save()

            # Limpiar la sesión
            del request.session['caja_abierta_id']

            return JsonResponse({'success': True, 'message': 'Precierre guardado con éxito.'})
        except AperturaCaja.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Caja abierta no encontrada.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)

# Cajaregistradora/views.py

def verificar_caja_abierta(request):
    caja_abierta_id = request.session.get('caja_abierta_id')
    if caja_abierta_id:
        try:
            apertura = AperturaCaja.objects.get(id=caja_abierta_id, abierta=True)
            datos = {
                'abierta': True,
                'cajero': apertura.cajero,
                'monto_inicial': str(apertura.monto_inicial),
                'fecha_hora_apertura': apertura.fecha_hora_apertura.strftime('%d/%m/%Y %H:%M:%S') if apertura.fecha_hora_apertura else 'No disponible',
            }
            return JsonResponse({'abierta': True, 'datos': datos})
        except AperturaCaja.DoesNotExist:
            return JsonResponse({'abierta': False})
    else:
        return JsonResponse({'abierta': False})
    
    
    
#Este Codigo esta estructurado por Berlin Cordero Brenes derecho de autor 2024 