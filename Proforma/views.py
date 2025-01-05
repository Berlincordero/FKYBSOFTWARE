from .models import Proforma,  DetalleProforma
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import subprocess
from django.shortcuts import render, redirect
from .forms import ProformaForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import requests



# Create your views here.

def lista_proforma(request):
    proformas = Proforma.objects.filter(activo=True)  
    return render(request, 'Proforma.html', {'proformas': proformas})




from django.shortcuts import render, get_object_or_404
from .models import Proforma, DetalleProforma

def editar_proforma(request, pk):
    proforma = get_object_or_404(Proforma, pk=pk)

    if request.method == 'POST':
        # 1) Actualiza los datos de cabecera
        proforma.fecha = request.POST.get('fecha')
        proforma.moneda = request.POST.get('moneda')
        proforma.cliente = request.POST.get('cliente')
        proforma.codigo_actividad_economica = request.POST.get('codigo_actividad_economica')
        proforma.medio_pago = request.POST.get('medio_pago')
        proforma.condicion_venta = request.POST.get('condicion_venta')
        proforma.detalles = request.POST.get('detalles')
        proforma.subtotal = float(request.POST.get('subtotal', 0.0) or 0.0)
        proforma.descuento = float(request.POST.get('descuento', 0.0) or 0.0)
        proforma.iva = float(request.POST.get('iva', 0.0) or 0.0)
        proforma.total = float(request.POST.get('total', 0.0) or 0.0)
        proforma.save()

        # Eliminar detalles viejos
        DetalleProforma.objects.filter(proforma=proforma).delete()

        # Crear de nuevo
        for key, value in request.POST.items():
            if key.startswith('cantidad_'):
                codigo_producto = key.split('_', 1)[1]
                cantidad = int(value)
                descuento_item = float(request.POST.get(f"descuento_{codigo_producto}", 0.0))
                precio_unitario = float(request.POST.get(f"precio_{codigo_producto}", 0.0))

                nombre_producto = request.POST.get(f"nombre_{codigo_producto}", codigo_producto)
                descripcion_producto = request.POST.get(f"descripcion_{codigo_producto}", "")

                sub_item = cantidad * precio_unitario
                monto_desc = (sub_item * descuento_item) / 100.0
                total_item = sub_item - monto_desc

                DetalleProforma.objects.create(
                    proforma=proforma,
                    producto=nombre_producto,
                    descripcion=descripcion_producto,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    descuento=monto_desc,
                    total=total_item
                )

        return redirect('lista_proforma')

    return redirect('lista_proforma')


def crear_proforma(request):
    if request.method == 'POST':
        # Obtén la cédula del cliente
        cedula = request.POST.get('cliente', '').strip()

        if not cedula:
            return render(request, 'Proforma.html', {
                'error': 'El campo "Cédula del Cliente" es obligatorio.'
            })

        # Llama a la API de Hacienda
        url = f"https://api.hacienda.go.cr/fe/ae?identificacion={cedula}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                nombre_cliente = data.get('nombre', '').strip()
                tipo_identificacion = data.get('tipoIdentificacion', '').strip()
                regimen = data.get('regimen', {}).get('descripcion', '').strip()
                situacion = data.get('situacion', {}).get('estado', '').strip()

                if not nombre_cliente:
                    return render(request, 'Proforma.html', {
                        'error': 'No se encontró información del cliente en Hacienda.'
                    })
            else:
                return render(request, 'Proforma.html', {
                    'error': f'Error al consultar Hacienda: {response.status_code}'
                })
        except Exception as e:
            return render(request, 'Proforma.html', {
                'error': f'Error al conectar con Hacienda: {str(e)}'
            })

        # Crear la proforma
        proforma = Proforma(
            fecha=request.POST.get('fecha'),
            moneda=request.POST.get('moneda'),
            cliente=nombre_cliente,  # Nombre del cliente
            tipo_identificacion=tipo_identificacion,  # Tipo de identificación
            regimen=regimen,  # Régimen del cliente
            situacion=situacion,  # Situación del cliente
            codigo_actividad_economica=request.POST.get('codigo_actividad_economica'),
            medio_pago=request.POST.get('medio_pago'),
            condicion_venta=request.POST.get('condicion_venta'),
            detalles=request.POST.get('detalles', ''),
            subtotal=float(request.POST.get('subtotal', 0.0) or 0.0),
            descuento=float(request.POST.get('descuento', 0.0) or 0.0),
            iva=float(request.POST.get('iva', 0.0) or 0.0),
            total=float(request.POST.get('total', 0.0) or 0.0),
        )
        proforma.save()

        # Guardar los productos de detalle de la proforma
        for key, value in request.POST.items():
            if key.startswith('cantidad_'):
                codigo_producto = key.split('_', 1)[1]
                cantidad = int(value)
                descuento_item = float(request.POST.get(f"descuento_{codigo_producto}", 0.0))
                precio_unitario = float(request.POST.get(f"precio_{codigo_producto}", 0.0))

                # Leer el nombre y descripción
                nombre_producto = request.POST.get(f"nombre_{codigo_producto}", codigo_producto)
                descripcion_producto = request.POST.get(f"descripcion_{codigo_producto}", "")

                sub_item = cantidad * precio_unitario
                monto_desc = (sub_item * descuento_item) / 100.0  # si desc_item es %
                total_item = sub_item - monto_desc

                DetalleProforma.objects.create(
                    proforma=proforma,
                    producto=nombre_producto,  # Guardamos el nombre
                    descripcion=descripcion_producto,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    descuento=monto_desc,  # Monto en colones
                    total=total_item
                )

        return redirect('lista_proforma')

    return render(request, 'Proforma.html')


def eliminar_proforma(request, pk):
    proforma = get_object_or_404(Proforma, pk=pk)
    proforma.activo = False  # Marca la proforma como inactiva
    proforma.save()
    return redirect('lista_proforma')  



def obtener_detalles_proforma(request, proforma_id):
    print("=== LLAMANDO obtener_detalles_proforma ===")  # <-- 
    proforma = get_object_or_404(Proforma, pk=proforma_id)
    detalles = DetalleProforma.objects.filter(proforma=proforma)
    data = []
    for d in detalles:
        data.append({
            "producto": d.producto,
            "descripcion": d.descripcion or "",
            "cantidad": d.cantidad,
            "precio_unitario": d.precio_unitario,
            "descuento": d.descuento,
            "total": d.total,
        })
    return JsonResponse(data, safe=False)