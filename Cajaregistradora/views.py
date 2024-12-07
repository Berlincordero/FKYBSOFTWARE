from django.conf import settings
from django.shortcuts import render
from .models import Factura
from datetime import datetime
from django.shortcuts import render
from Inventario.models import Producto

from django.conf import settings
from django.shortcuts import render


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

    # Generar la fecha y hora actual
    fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Formato: YYYY-MM-DD HH:MM:SS

    # Generar número de factura
    from .models import Factura
    last_factura = Factura.objects.last()
    if last_factura:
        last_number = int(last_factura.numero_factura.split()[1])  # Obtiene el último número
    else:
        last_number = 0
    numero_factura = f"F {last_number + 1}"  # Genera el siguiente número

    # Agregar la fecha, hora y el número de factura al contexto
    context = {
        'terminal': terminal,
        'sucursal': sucursal,
        'productos': productos,
        'fecha_hora_actual': fecha_hora_actual,
        'numero_factura': numero_factura,
    }

    return render(request, 'Cajaregistradora.html', context)