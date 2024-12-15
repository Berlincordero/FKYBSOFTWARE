from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from .models import OrdenDeCompra
from Proveedores.models import Proveedor
from .forms import OrdenDeCompraForm  
from decimal import Decimal
from django.views.decorators.http import require_POST
from io import BytesIO
from django.http import HttpResponse
from xhtml2pdf import pisa


def lista_ordenes(request):
    ordenes = OrdenDeCompra.objects.filter(activo=True)  # Filtrar órdenes activas
    proveedores = Proveedor.objects.filter(activo=True)  # Obtener todos los proveedores activos
    metodos_pago = ['EFECTIVO', 'TARJETA', 'SINPE']  # Métodos de pago disponibles

    if request.method == 'POST':
        form = OrdenDeCompraForm(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad']
            precio_unitario = form.cleaned_data['precio_unitario']
            total = cantidad * precio_unitario

            orden = form.save(commit=False)
            orden.usuario = request.user.username  # Asignar el usuario actual
            orden.total = total
            orden.save()
            return redirect('lista_ordenes')  # Redirigir después de guardar
    else:
        form = OrdenDeCompraForm()

    context = {
        'ordenes': ordenes,
        'proveedores': proveedores,  # Pasar los proveedores al template
        'metodos_pago': metodos_pago,
        'form': form,
    }
    return render(request, 'ordenes/orden_de_compra.html', context)




@require_POST
def eliminar_orden(request):
    orden_id = request.POST.get('orden_id')
    orden = get_object_or_404(OrdenDeCompra, id_orden=orden_id)
    orden.activo = False  # Marca la orden como inactiva
    orden.save()  # Guarda el cambio en la base de datos
    return redirect('lista_ordenes')

@require_POST
def editar_orden(request):
    if request.method == 'POST':
        orden_id = request.POST.get('orden_id')
        try:
            orden = OrdenDeCompra.objects.get(id_orden=orden_id)
            orden.usuario = request.user.username  # Asignar el usuario actual
            orden.producto = request.POST.get('producto')
            orden.descripcion = request.POST.get('descripcion')
            orden.cantidad = int(request.POST.get('cantidad'))
            orden.precio_unitario = float(request.POST.get('precio_unitario'))
            orden.proveedor = Proveedor.objects.get(id_proveedor=request.POST.get('proveedor'))
            orden.metodo_pago = request.POST.get('metodo_pago')
            orden.notas = request.POST.get('notas')

            # Calcular el total nuevamente
            orden.total = orden.cantidad * orden.precio_unitario

            orden.save()  # Guardar los cambios
            return redirect('lista_ordenes')
        except OrdenDeCompra.DoesNotExist:
            # Manejar el error de que no existe la orden
            return redirect('lista_ordenes')  # O redirigir a una página de error

def detalle_orden(request, orden_id):
    orden = get_object_or_404(OrdenDeCompra, id=orden_id)
    return render(request, 'ordenes/detalle_orden.html', {
        'orden': orden,    
    })
    
    
def descargar_orden_pdf(request, id):
    try:
        orden = OrdenDeCompra.objects.get(id_orden=id)
        
        # Detalles de la empresa
        empresa = {
            'nombre': "Ferretería San Jerónimo",
            'descripcion': "Proveedor de materiales para la construcción. Amplia gama de productos, incluye material pesado, madera, gypsum, pinturas...",
            'direccion': "San Jerónimo, Moravia, San Jerónimo, Costa Rica",
            'telefono': "2229 3181",
            'email': "sanjeronimoferreteria@gmail.com",
        }

        # Plantilla HTML para el PDF
        html = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th, td {{
                    padding: 8px;
                    text-align: left;
                    border: 1px solid #ddd;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
                .encabezado {{
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .footer {{
                    margin-top: 30px;
                    text-align: center;
                    font-size: 12px;
                    color: #555;
                }}
            </style>
        </head>
        <body>
            <div class="encabezado">
                <h2>{empresa['nombre']}</h2>
                <p>{empresa['descripcion']}</p>
                <p><strong>Dirección:</strong> {empresa['direccion']}</p>
                <p><strong>Teléfono:</strong> {empresa['telefono']} | <strong>Email:</strong> {empresa['email']}</p>
            </div>
            <h3 style="text-align: center;">Orden de Compra N° {orden.id_orden}</h3>
            <table>
                <tr>
                    <th>Usuario:</th>
                    <td>{orden.usuario}</td>
                </tr>
                <tr>
                    <th>Proveedor:</th>
                    <td>{orden.proveedor.nombre_empresa}</td>
                </tr>
                <tr>
                    <th>Fecha:</th>
                    <td>{orden.fecha_orden.strftime('%d/%m/%Y')}</td>
                </tr>
                <tr>
                    <th>Producto:</th>
                    <td>{orden.producto}</td>
                </tr>
                <tr>
                    <th>Descripción:</th>
                    <td>{orden.descripcion}</td>
                </tr>
                <tr>
                    <th>Cantidad:</th>
                    <td>{orden.cantidad}</td>
                </tr>
                <tr>
                    <th>Precio Unitario:</th>
                    <td>{orden.precio_unitario:.2f} CRC</td>
                </tr>
                <tr>
                    <th>Total:</th>
                    <td>{orden.total:.2f} CRC</td>
                </tr>
                <tr>
                    <th>Método de Pago:</th>
                    <td>{orden.metodo_pago}</td>
                </tr>
                <tr>
                    <th>Notas:</th>
                    <td>{orden.notas}</td>
                </tr>
            </table>
            <div class="footer">
                <p>Gracias por confiar en {empresa['nombre']}.</p>
                <p>Este documento fue generado automáticamente y no requiere firma.</p>
            </div>
        </body>
        </html>
        """

        # Generar el PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="orden_{orden.id_orden}.pdf"'
        pisa_status = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=response, encoding='UTF-8')

        if pisa_status.err:
            return HttpResponse(f"Error al generar el PDF: {pisa_status.err}")
        return response
    except OrdenDeCompra.DoesNotExist:
        return HttpResponse("Orden no encontrada", status=404)
    
    