from django.shortcuts import render
from Cajaregistradora.models import Factura
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.timezone import now
from Cajaregistradora.models import PreCierre
import pandas as pd
import openpyxl


def facturacion(request):
    facturas = Factura.objects.all()  # Obtener todas las facturas
    context = {"facturas": facturas}
    return render(request, 'Facturacion/facturacion.html', context)


def PrecierreCaja(request):
    # Recupera todos los registros de PreCierre para mostrarlos en la tabla
    precierres = PreCierre.objects.all()
    return render(request, "Facturacion/PrecierreCaja.html", {"precierres": precierres})


def exportar_precierres_excel(request):
    # Recuperar todos los precierres
    precierres = PreCierre.objects.all().values(
        'sucursal',
        'caja_registradora',
        'hora_apertura',
        'fecha',
        'monto_inicial',
        'cajero',
        'impuestos',
        'efectivo',
        'facturas_proveedor',
        'tarjetas',
        'simpe_movil',
        'venta_credito',
        'movimientos',
        'total_ventas',
        'cantidad_facturas',
        'conteo_efectivo',
        'conteo_tarjetas',
        'contado_efectivo',
        'contado_tarjetas',
    )

    # Convertir a DataFrame
    df = pd.DataFrame(list(precierres))

    # Crear una respuesta HTTP con el contenido del archivo Excel
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=precierres.xlsx'

    # Escribir el DataFrame en la respuesta como un archivo Excel
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Precierres')

    return response

  # Opcional: asegura que solo usuarios autenticados puedan acceder
def exportar_facturas_excel(request):
    # Crear un libro de trabajo de Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Facturas"

    # Añadir encabezados
    headers = [
        'Fecha', 'Número Factura', 'Cliente', 'Código', 
        'Descripción', 'Cantidad', 'Precio Venta', 'I.V.A', 
        'Total', 'Estado de la Factura'
    ]
    ws.append(headers)

    # Obtener todas las facturas
    facturas = Factura.objects.all()

    # Verifica si hay facturas
    if not facturas.exists():
        ws.append(["No hay facturas disponibles"])
    else:
        # Añadir filas de facturas
        for factura in facturas:
            ws.append([
                factura.fecha.strftime('%Y-%m-%d') if factura.fecha else '',
                factura.numero_factura or '',
                factura.cliente or '',
                factura.codigo or '',
                factura.descripcion or '',
                factura.cantidad or 0,
                factura.precio_venta or 0.0,
                factura.iva or 0.0,
                factura.total or 0.0,
                factura.estado_factura or '',
        
            ])

    # Definir la respuesta HTTP con el tipo de contenido de Excel
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=facturas.xlsx'

    # Guardar el archivo Excel en la respuesta
    wb.save(response)

    return response

