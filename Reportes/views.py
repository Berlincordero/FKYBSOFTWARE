from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import CuentaPorCobrar, PagoFactura
from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from Proforma.models import Proforma
from Cajaregistradora.models import Factura
from Inventario.models import Producto
from transportes.models import Ruta
from django.utils import timezone  
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.utils.timezone import now, timedelta
from datetime import datetime
from reportlab.pdfgen import canvas
from django.http import JsonResponse
from decimal import Decimal







# Create your views here.

pdfmetrics.registerFont(TTFont('DejaVuSans', 'static/fonts/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'static/fonts/DejaVuSans-Bold.ttf'))

@login_required
def ventas(request):
    # Calcular los últimos 6 meses por defecto
    end_date = now()
    start_date = end_date - timedelta(days=6 * 30)

    # Verificar si el usuario seleccionó fechas en el filtro
    start_date_param = request.GET.get('start_date')
    end_date_param = request.GET.get('end_date')

    if start_date_param and end_date_param:
        try:
            start_date = datetime.strptime(start_date_param, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_param, "%Y-%m-%d")
        except ValueError:
            return JsonResponse({'error': 'Fechas inválidas.'}, status=400)

    # Filtrar facturas en el rango seleccionado
    facturas = Factura.objects.filter(fecha__date__gte=start_date, fecha__date__lte=end_date)

    # Calcular ventas por mes
    ventas_por_mes = {}
    for factura in facturas:
        mes = factura.fecha.strftime('%B %Y')
        ventas_por_mes[mes] = ventas_por_mes.get(mes, 0) + float(factura.total)

    # Renderizar la plantilla
    context = {
        'facturas': facturas,
        'ventas_por_mes': ventas_por_mes,
        'start_date': start_date.strftime("%Y-%m-%d"),
        'end_date': end_date.strftime("%Y-%m-%d"),
    }
    return render(request, 'Reportes/ventas.html', context)
@login_required
def obtener_factura(request, numero_factura):
    try:
        factura = Factura.objects.get(numero_factura=numero_factura)
        data = {
            "fecha": factura.fecha.strftime('%Y-%m-%d'),
            "numero_factura": factura.numero_factura,
            "cliente": factura.cliente or "Cliente Desconocido",
            "codigo": factura.codigo,
            "nombre": factura.nombre,
            "descripcion": factura.descripcion,
            "cantidad": factura.cantidad,
            "precio_venta": float(factura.precio_venta),
            "iva": float(factura.iva),
            "total": float(factura.total),
            "estado_factura": factura.estado_factura,
            "tipo_pago": factura.tipo_pago,
        }
        return JsonResponse(data)
    except Factura.DoesNotExist:
        return JsonResponse({"error": "Factura no encontrada."}, status=404)


@login_required
def cuentasCobrar(request):
    if request.method == 'POST':
        # Procesar el formulario
        cliente = request.POST.get('clientName')
        monto = request.POST.get('amount')
        fecha_vencimiento = request.POST.get('dueDate')
        descripcion = request.POST.get('description')

        # Guardar la cuenta por cobrar
        CuentaPorCobrar.objects.create(
            cliente=cliente,
            monto=monto,
            fecha_vencimiento=fecha_vencimiento,
            descripcion=descripcion
        )

        # Redirigir a la misma página después de registrar
        return redirect('cuentasCobrar')

    # Manejar solicitudes GET
    cuentas = CuentaPorCobrar.objects.all()
    return render(request, 'Reportes/cuentasCobrar.html', {'cuentas': cuentas})



@login_required
def pagosFacturas(request):
    if request.method == 'POST':
        numero_factura = request.POST.get('invoiceNumber')
        monto_pago = request.POST.get('paymentAmount')
        fecha_pago = request.POST.get('paymentDate')
        metodo_pago = request.POST.get('paymentMethod')

        if numero_factura and monto_pago and fecha_pago and metodo_pago:
            PagoFactura.objects.create(
                numero_factura=numero_factura,
                monto_pago=monto_pago,
                fecha_pago=fecha_pago,
                metodo_pago=metodo_pago
            )
            return redirect('pagosFacturas')  

    pagos = PagoFactura.objects.all()
    return render(request, 'Reportes/pagosFacturas.html', {'pagos': pagos})
@login_required
def reporteUtilidades(request):
    # Calcular fechas por defecto (1 año atrás desde hoy)
    end_date = now()
    start_date = end_date - timedelta(days=365)

    # Obtener fechas desde los parámetros GET
    start_date_param = request.GET.get('start_date')
    end_date_param = request.GET.get('end_date')

    if start_date_param and end_date_param:
        try:
            start_date = datetime.strptime(start_date_param, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_param, "%Y-%m-%d")
        except ValueError:
            return HttpResponse("Fechas inválidas.", status=400)

    # Obtener facturas en el rango de fechas
    facturas = Factura.objects.filter(fecha__gte=start_date, fecha__lte=end_date)

    # Calcular totales
    ingresos_totales = sum(factura.total for factura in facturas)
    iva_total = sum(factura.iva for factura in facturas)
    
    # Calcular costo total basado en productos vendidos
    costo_total_productos = 0
    for factura in facturas:
        try:
            producto = Producto.objects.get(codigo_cabys=factura.codigo)
            costo_total_productos += producto.precio_costo * factura.cantidad
        except Producto.DoesNotExist:
            continue

    # Calcular utilidades netas (ingresos - costos - IVA)
    utilidades_netas = ingresos_totales - costo_total_productos - iva_total

    context = {
        'facturas': facturas,
        'ingresos_totales': ingresos_totales,
        'costo_total_productos': costo_total_productos,
        'iva_total': iva_total,
        'utilidades_netas': utilidades_netas,
        'start_date': start_date.strftime("%Y-%m-%d"),
        'end_date': end_date.strftime("%Y-%m-%d"),
    }

    return render(request, 'Reportes/reporteUtilidades.html', context)

@login_required
def cierreCaja(request):
    return render(request, 'Reportes/cierreCaja.html')
@login_required
def reporteProformas(request):
    # Obtén todas las proformas con sus detalles
    proformas = Proforma.objects.prefetch_related('detalle_proformas')

    # Prepara los datos para el reporte
    reporte = []
    for proforma in proformas:
        detalles = proforma.detalle_proformas.all()  # Asegúrate de usar el related_name correcto
        subtotal = sum(detalle.total for detalle in detalles)
        descuento = sum(detalle.descuento for detalle in detalles)
        iva = subtotal * 0.13
        total = subtotal - descuento + iva
        reporte.append({
            'proforma': proforma,
            'detalles': detalles,
            'subtotal': subtotal,
            'descuento': descuento,
            'iva': iva,
            'total': total,
        })

    # Renderiza la plantilla con el reporte
    return render(request, 'Reportes/reporteProformas.html', {'reporte': reporte})


@login_required
def detalles_proforma(request, pk):
    try:
        proforma = Proforma.objects.get(pk=pk)
        detalles = proforma.detalle_proformas.all()
        detalles_data = [
            {
                'producto': detalle.producto,
                'descripcion': detalle.descripcion,
                'cantidad': detalle.cantidad,
                'precio_unitario': detalle.precio_unitario,
                'descuento': detalle.descuento,
                'total': detalle.total,
            }
            for detalle in detalles
        ]
        return JsonResponse({'detalles': detalles_data})
    except Proforma.DoesNotExist:
        return JsonResponse({'error': 'Proforma no encontrada'}, status=404)

@login_required
def reporteTransportes(request):
    # Obtener todas las rutas activas
    rutas = Ruta.objects.select_related('nombre_conductor', 'id_vehiculo').all()

    context = {
        'rutas': rutas,
    }
    return render(request, 'Reportes/reporteTransportes.html', context)
@login_required
def generar_pdf_cuentas_por_cobrar(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_cuentas_por_cobrar.pdf"'

    pdf = SimpleDocTemplate(response, pagesize=letter)

    title = [['Reporte de Cuentas por Cobrar']]
    title_table = Table(title)
    title_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
        ('FONTSIZE', (0, 0), (-1, -1), 16),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12)
    ]))

    data = [['Cliente', 'Monto (₡)', 'Fecha de Vencimiento', 'Estado']]
    cuentas = CuentaPorCobrar.objects.all()
    total_monto = 0

    for cuenta in cuentas:
        data.append([
            cuenta.cliente,
            f"₡{cuenta.monto:.2f}",
            cuenta.fecha_vencimiento.strftime('%Y-%m-%d'),
            cuenta.estado.capitalize()
        ])
        total_monto += cuenta.monto

    data.append(['Total', f"₡{total_monto:.2f}", '', ''])

    table = Table(data, colWidths=[150, 150, 150, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans'),  
        ('FONTNAME', (0, 1), (-1, -1), 'DejaVuSans'),  
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, -1), (-1, -1), 'DejaVuSans-Bold'),  
    ]))

    pdf.build([title_table, table])

    return response
@login_required
def generar_pdf_pagos_facturas(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_pagos_facturas.pdf"'

    pdf = SimpleDocTemplate(response, pagesize=letter)

    title = [['Reporte de Pagos a Facturas']]
    title_table = Table(title)
    title_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
        ('FONTSIZE', (0, 0), (-1, -1), 16),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12)
    ]))

    data = [['Número de Factura', 'Monto del Pago (₡)', 'Fecha del Pago', 'Método de Pago']]
    pagos = PagoFactura.objects.all()

    for pago in pagos:
        data.append([
            pago.numero_factura,
            f"₡{pago.monto_pago:.2f}", 
            pago.fecha_pago.strftime('%Y-%m-%d'),
            pago.metodo_pago.capitalize()
        ])

    table = Table(data, colWidths=[150, 150, 150, 150])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans'),  
        ('FONTNAME', (0, 1), (-1, -1), 'DejaVuSans'),  
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    pdf.build([title_table, table])

    return response
@login_required
def generar_pdf_proforma_detalle(request, proforma_id):
    proforma = get_object_or_404(Proforma, id=proforma_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="proforma_{proforma_id}.pdf"'

    pdf = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()

    title = [['Detalle de Proforma']]
    title_table = Table(title)
    title_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
        ('FONTSIZE', (0, 0), (-1, -1), 16),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12)
    ]))

    header_data = [
        ['Fecha:', proforma.fecha.strftime('%Y-%m-%d')],
        ['Cliente:', proforma.cliente],
        ['Moneda:', proforma.moneda],
        ['Código de Actividad Económica:', proforma.codigo_actividad_economica],
        ['Medio de Pago:', proforma.medio_pago],
        ['Condición de Venta:', proforma.condicion_venta],
        ['Nota:', proforma.nota],
    ]
    header_table = Table(header_data, colWidths=[200, 300])
    header_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))

    details_data = [['Descripción', 'Subtotal (₡)', 'Descuento (₡)', 'IVA (₡)', 'Total (₡)']]
    details_data.append([
        proforma.detalles,
        f"₡{proforma.subtotal:.2f}",
        f"₡{proforma.descuento:.2f}",
        f"₡{proforma.iva:.2f}",
        f"₡{proforma.total:.2f}"
    ])
    details_table = Table(details_data, colWidths=[200, 100, 100, 100, 100])
    details_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    pdf.build([title_table, header_table, details_table])

    return response
@login_required
def generar_pdf_transportes(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_transportes.pdf"'

    pdf = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    title = Paragraph("Reporte de Todas las Rutas Registradas", styles['Title'])
    elements.append(title)

    generation_date = Paragraph(f"Fecha de Generación: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
    elements.append(generation_date)

    elements.append(Spacer(1, 12))

    rutas = Ruta.objects.select_related('nombre_conductor', 'id_vehiculo').all()

    if rutas.exists():
        for ruta in rutas:
            ruta_title = Paragraph(f"ID Ruta: {ruta.id_ruta}", styles['Heading2'])
            elements.append(ruta_title)

            data = [
                ["Fecha", ruta.fecha_ruta.strftime('%Y-%m-%d')],
                ["Provincia", ruta.provincia],
                ["Cantón", ruta.canton],
                ["Distrito", ruta.distrito],
                ["Dirección Exacta", ruta.direccion_exacta],
                ["Conductor", f"{ruta.nombre_conductor.nombre_conductor} {ruta.nombre_conductor.apellidos_1} {ruta.nombre_conductor.apellidos_2}"],
                ["Vehículo", f"{ruta.id_vehiculo.marca} {ruta.id_vehiculo.modelo} ({ruta.id_vehiculo.id_vehiculo})"],
            ]

            table = Table(data, colWidths=[120, 400])  # Ajustar anchos de columnas
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.grey),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))

            elements.append(table)
            elements.append(Spacer(1, 20)) 
    else:
        no_data = Paragraph("No se encontraron rutas registradas.", styles['Normal'])
        elements.append(no_data)

    pdf.build(elements)
    return response
@login_required
def descargar_reporte_ventas(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if not start_date or not end_date:
        return HttpResponse("Por favor selecciona un rango de fechas válido.", status=400)

    # Convertir fechas
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        return HttpResponse("Formato de fecha inválido.", status=400)

    # Obtener facturas en el rango
    facturas = Factura.objects.filter(fecha__date__gte=start_date, fecha__date__lte=end_date)

    # Crear el reporte en PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_ventas_detallado.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Encabezado del reporte
    encabezado = f"Reporte de Ventas - Facturas Detalladas\nDesde: {start_date.strftime('%Y-%m-%d')} Hasta: {end_date.strftime('%Y-%m-%d')}"
    elements.append(Paragraph(encabezado, getSampleStyleSheet()['Heading2']))

    # Crear tabla con las facturas
    data = [["Fecha", "N° Factura", "Total ($)"]]
    total_general = 0
    for factura in facturas:
        data.append([
            factura.fecha.strftime('%Y-%m-%d'),
            factura.numero_factura,
            f"${factura.total:.2f}"
        ])
        total_general += float(factura.total)

    # Agregar total general
    data.append(["", "TOTAL GENERAL", f"${total_general:.2f}"])

    # Estilizar la tabla
    table = Table(data, colWidths=[100, 150, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)

    # Generar PDF
    doc.build(elements)
    return response

@login_required
def descargar_factura(request, numero_factura):
    factura = get_object_or_404(Factura, numero_factura=numero_factura)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factura_{factura.numero_factura}.pdf"'

    c = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Ferretería San Jerónimo")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 70, "San Jerónimo, Moravia, San Jerónimo, Costa Rica")
    c.drawString(50, height - 85, "Teléfono: 2229 3181")
    c.drawString(50, height - 100, "Correo: sanjeronimoferreteria@gmail.com")

    c.line(50, height - 110, width - 50, height - 110)

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 130, "Factura Detallada")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 150, f"Factura ID: {factura.numero_factura}")
    c.drawString(50, height - 165, f"Fecha: {factura.fecha.strftime('%Y-%m-%d')}")
    c.drawString(50, height - 180, f"Cliente: {factura.cliente or 'Cliente Desconocido'}")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 210, "Detalles del Producto")
    c.setFont("Helvetica", 11)
    y = height - 230
    c.drawString(50, y, f"Código: {factura.codigo}")
    y -= 20
    c.drawString(50, y, f"Nombre: {factura.nombre}")
    y -= 20
    c.drawString(50, y, f"Descripción: {factura.descripcion}")
    y -= 20
    c.drawString(50, y, f"Cantidad: {factura.cantidad}")
    y -= 20
    c.drawString(50, y, f"Precio Unitario: ${factura.precio_venta:.2f}")
    y -= 20
    c.drawString(50, y, f"IVA: ${factura.iva:.2f}")
    y -= 20
    c.drawString(50, y, f"Total: ${factura.total:.2f}")

    y -= 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Detalles de la Factura")
    c.setFont("Helvetica", 11)
    y -= 20
    c.drawString(50, y, f"Estado de la Factura: {factura.estado_factura}")
    y -= 20
    c.drawString(50, y, f"Tipo de Pago: {factura.tipo_pago}")

    c.save()
    return response


@login_required
def descargar_reporte_utilidades(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Fechas por defecto: último año
    if not start_date or not end_date:
        end_date = now()
        start_date = end_date - timedelta(days=365)
    else:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

    facturas = Factura.objects.filter(fecha__gte=start_date, fecha__lte=end_date)

    ingresos_totales = sum(factura.total for factura in facturas)
    iva_total = sum(factura.iva for factura in facturas)
    costo_total_productos = sum(
        Producto.objects.get(codigo_cabys=factura.codigo).precio_costo * factura.cantidad
        for factura in facturas if Producto.objects.filter(codigo_cabys=factura.codigo).exists()
    )
    utilidades_netas = ingresos_totales - costo_total_productos - iva_total

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_utilidades_{start_date.strftime("%Y%m%d")}_{end_date.strftime("%Y%m%d")}.pdf"'

    c = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    c.setFont("DejaVuSans-Bold", 16)
    c.drawString(50, height - 50, "Reporte de Utilidades")

    c.setFont("DejaVuSans", 12)
    c.drawString(50, height - 80, f"Periodo: {start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}")

    data = [
        ["Concepto", "Monto (COLONES)"],
        ["Ingresos Totales", f"₡ {ingresos_totales:,.2f}"],
        ["Costo Total de Productos", f"₡ {costo_total_productos:,.2f}"],
        ["IVA Total", f"₡ {iva_total:,.2f}"],
        ["Utilidades Netas", f"₡ {utilidades_netas:,.2f}"]
    ]

    table = Table(data, colWidths=[200, 150])
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4CAF50")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'DejaVuSans'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table.setStyle(style)

    table.wrapOn(c, width, height)
    table.drawOn(c, 50, height - 200)

    c.setFont("DejaVuSans", 10)
    c.drawString(50, 50, "Generado automáticamente por el sistema de reportes de Ferretería San Jerónimo.")
    c.save()
    return response


