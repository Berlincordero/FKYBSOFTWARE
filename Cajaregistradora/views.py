from django.conf import settings
from django.shortcuts import render
from .models import Factura
from datetime import datetime


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    # Ajustar para entorno local
    if ip == '127.0.0.1':
        ip = '192.168.0.101'  # IP única de terminal local
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

    # Crear una factura para prueba
    factura = Factura.objects.create(
        cliente="Cliente de Prueba",
        codigo="PRUEBA001",
        nombre="Producto de Prueba",
        descripcion="Una descripción breve",
        cantidad=1,
        precio_venta=100.00,
        iva=13.00,
        total=113.00
    )

    # Obtener la fecha actual
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return render(request, 'Cajaregistradora.html', {
        'terminal': terminal,
        'sucursal': sucursal,
        'numero_factura': factura.numero_factura,
        'fecha_actual': fecha_actual,  # Enviar la fecha al contexto
    })