from django.shortcuts import render, get_object_or_404
import openpyxl
from django.http import HttpResponse
from .models import Producto
import os
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import subprocess
from django.http import JsonResponse
from .forms import ProductoForm 
from django.shortcuts import render, redirect
from .models import Producto
from .forms import ProductoForm

# Create your views here.
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'Inventario.html', {'productos': productos})


def crear_producto(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.POST.get('nombreProducto')
        cantidad = request.POST.get('cantidadProducto')
        descripcion = request.POST.get('descripcionProducto')
        codigo_cabys = request.POST.get('codigoCABYS')
        moneda = request.POST.get('monedaProducto')
        precio_costo = request.POST.get('precioCosto')
        precio_venta = request.POST.get('precioVenta')
        descuento = request.POST.get('descuentoProducto')
        clasificacion = request.POST.get('clasificacionProducto')
        
        # Crear el nuevo producto
        producto = Producto.objects.create(
            nombre=nombre,
            cantidad=cantidad,
            descripcion=descripcion,
            codigo_cabys=codigo_cabys,
            moneda=moneda,
            precio_costo=precio_costo,
            precio_venta=precio_venta,
            descuento=descuento,
            clasificacion=clasificacion
        )
        producto.save()
        return redirect('lista_productos')

def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'editar_producto.html', {'form': form})


def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return redirect('lista_productos')


def exportar_productos_excel(request):
    # Crear un archivo Excel en memoria
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Productos"

    # Añadir encabezados
    headers = [
        'Nombre', 'Cantidad','Descripción', 'Código CABYS', 
        'Moneda', 'Precio del Costo', 'Precio de Venta', 'Descuento', 
        'Clasificación'
    ]
    ws.append(headers)

    # Obtener los productos del modelo
    productos = Producto.objects.all()

    # Verifica si hay productos
    if not productos.exists():
        ws.append(["No hay productos en el inventario"])
    else:
        # Añadir filas de productos
        for producto in productos:
            ws.append([
                producto.nombre or '',
                producto.cantidad or 0,
                producto.descripcion or '',
                producto.codigo_cabys or '',
                producto.moneda or '',
                producto.precio_costo or 0.0,
                producto.precio_venta or 0.0,
                producto.descuento or 0,
                producto.clasificacion or '',
                
            ])

    # Definir la respuesta HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="productos.xlsx"'

    # Guardar el archivo Excel en la respuesta
    wb.save(response)

    return response


def subir_bd_pgsql(request):
    if request.method == 'POST' and request.FILES['archivo_pgsql']:
        archivo_pgsql = request.FILES['archivo_pgsql']
        fs = FileSystemStorage()
        nombre_archivo = fs.save(archivo_pgsql.name, archivo_pgsql)
        ruta_archivo = fs.path(nombre_archivo)
        
        # Datos de conexión a la base de datos desde settings.py
        db_name = settings.DATABASES['default']['NAME']
        db_user = settings.DATABASES['default']['USER']
        db_password = settings.DATABASES['default']['PASSWORD']
        db_host = settings.DATABASES['default']['HOST']
        db_port = settings.DATABASES['default']['PORT']
        
        # Comando para restaurar el archivo SQL o dump en PostgreSQL
        comando = f'PGPASSWORD={db_password} psql -h {db_host} -U {db_user} -d {db_name} -p {db_port} -f "{ruta_archivo}"'
        
        try:
            # Ejecutar el comando en el shell
            subprocess.run(comando, shell=True, check=True)
            return redirect('pagina_exito')  # Redirigir después de éxito
        except subprocess.CalledProcessError as e:
            print(f"Error ejecutando el archivo SQL: {e}")
            return render(request, 'error_carga.html', {'error': str(e)})
    
    return render(request, 'cargar_bd.html')