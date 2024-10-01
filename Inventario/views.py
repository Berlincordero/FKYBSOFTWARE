from django.shortcuts import render
import openpyxl
from django.http import HttpResponse
from .models import Producto
import os
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import subprocess


# Create your views here.


def Inventario_view(request):
    return render(request, 'Inventario.html')


def exportar_productos_excel(request):
    # Crear un archivo Excel en memoria
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Productos"

    # Añadir encabezados
    headers = [
        'Nombre', 'Cantidad', 'Unidad de Medida', 'Descripción', 'Código CABYS', 
        'Moneda', 'Precio del Costo', 'Precio de Venta', 'Descuento', 
        'Clasificación', 'Impuesto', 'Inventario Seguimiento'
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
                producto.unidad_medida or '',
                producto.descripcion or '',
                producto.codigo_cabys or '',
                producto.moneda or '',
                producto.precio_costo or 0.0,
                producto.precio_venta or 0.0,
                producto.descuento or 0,
                producto.clasificacion or '',
                producto.impuesto or '',
                "Sí" if producto.inventario_seguimiento else "No",
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