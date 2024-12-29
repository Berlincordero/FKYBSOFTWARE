from django.shortcuts import render
from Cajaregistradora.models import Factura
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.timezone import now
from Cajaregistradora.models import PreCierre
import pandas as pd
import openpyxl
from django.db.models import Sum
from decimal import Decimal

def facturacion(request):
    # 1. Obtenemos todas las facturas ordenadas
    qs_facturas = Factura.objects.all().order_by('numero_factura', 'fecha')

    # 2. Estructura para agrupar
    facturas_agrupadas = {}

    for f in qs_facturas:
        key = (f.numero_factura, f.fecha.date()) 
        # ^ Puede ser solo f.numero_factura si no necesitas agrupar por fecha

        if key not in facturas_agrupadas:
            facturas_agrupadas[key] = {
                'fecha': f.fecha,
                'numero_factura': f.numero_factura,
                'cliente': f.cliente,
                'estado_factura': f.estado_factura,
                'codigos_str': [],
                'descripciones_str': [],
                'cantidades_str': [],
                'precios_str': [],
                'iva_total': Decimal('0.00'),
                'total_final': Decimal('0.00')
            }

        # Concatenamos la info de cada ítem para esa factura
        facturas_agrupadas[key]['codigos_str'].append(str(f.codigo))
        facturas_agrupadas[key]['descripciones_str'].append(f.descripcion)
        facturas_agrupadas[key]['cantidades_str'].append(str(f.cantidad))
        facturas_agrupadas[key]['precios_str'].append(str(f.precio_venta))

        # Sumamos IVA y total para mostrar un “total final” por factura
        facturas_agrupadas[key]['iva_total'] += f.iva
        facturas_agrupadas[key]['total_final'] += f.total

    # 3. Convertir esos valores a una lista de facturas agrupadas
    facturas_resultado = []
    for key, datos in facturas_agrupadas.items():
        # Convertir las listas en un solo string. Por ejemplo, “código1, código2, ...”
        codigos_joined = ", ".join(datos['codigos_str'])
        descripciones_joined = ", ".join(datos['descripciones_str'])
        cantidades_joined = ", ".join(datos['cantidades_str'])
        precios_joined = ", ".join(datos['precios_str'])

        facturas_resultado.append({
            'fecha': datos['fecha'],
            'numero_factura': datos['numero_factura'],
            'cliente': datos['cliente'],
            'estado_factura': datos['estado_factura'],

            # Deja en un solo string todos los codigos, descripciones, etc.
            'codigos': codigos_joined,
            'descripciones': descripciones_joined,
            'cantidades': cantidades_joined,
            'precios_venta': precios_joined,

            'iva_total': datos['iva_total'],
            'total_final': datos['total_final']
        })

    context = {'facturas': facturas_resultado}
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

