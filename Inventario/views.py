from django.shortcuts import render, get_object_or_404
import openpyxl
from django.http import HttpResponse
from .models import Producto
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import subprocess
from django.shortcuts import render, redirect
from .models import Producto
from django.http import JsonResponse




# Create your views here.
def lista_productos(request):
    productos = Producto.objects.filter(activo=True)
    print(productos)
    return render(request, 'Inventario.html', {'productos': productos})

def editar_producto(request):
    if request.method == 'POST':
        # Obtén el pk del producto desde el formulario
        pk = request.POST.get('producto_id')
        producto = get_object_or_404(Producto, pk=pk)
        
        # Actualiza los campos según los datos enviados
        producto.nombre = request.POST.get('nombreProducto')
        producto.cantidad = request.POST.get('cantidadProducto')
        producto.unidad_medida = request.POST.get('unidadMedidaProducto')
        producto.descripcion = request.POST.get('descripcionProducto') 
        producto.codigo_cabys = request.POST.get('codigoCABYS')  
        producto.moneda = request.POST.get('monedaProducto')  
        producto.precio_costo = request.POST.get('precioCosto') 
        producto.precio_venta = request.POST.get('precioVenta')  
        producto.clasificacion = request.POST.get('clasificacionProducto')  

        producto.save()
        return redirect('lista_productos')

    return render(request, 'Inventario.html')


def crear_producto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombreProducto')
        cantidad = request.POST.get('cantidadProducto')
        unidad_medida = request.POST.get('unidadMedidaProducto')
        descripcion = request.POST.get('descripcionProducto')
        codigo_cabys = request.POST.get('codigoCABYS')
        moneda = request.POST.get('monedaProducto')
        precio_costo = request.POST.get('precioCosto')
        precio_venta = request.POST.get('precioVenta')
        clasificacion = request.POST.get('clasificacionProducto')
        
        # Crear el nuevo producto
        producto = Producto.objects.create(
            nombre=nombre,
            cantidad=cantidad,
            unidad_medida=unidad_medida,
            descripcion=descripcion,
            codigo_cabys=codigo_cabys,
            moneda=moneda,
            precio_costo=precio_costo,
            precio_venta=precio_venta,
            clasificacion=clasificacion
        )
        producto.save()
        return redirect('lista_productos')





def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    producto.activo = False  # Marca la proforma como inactiva
    producto.save()
    return redirect('lista_productos')  




def obtener_productos(request):
    # Filtramos productos activos para mostrarlos en el modal
    productos = Producto.objects.filter(activo=True).values('id', 'codigo_cabys', 'nombre', 'descripcion', 'precio_venta')
    return JsonResponse(list(productos), safe=False)




def exportar_productos_excel(request):
    # Crear un archivo Excel en memoria
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Productos"

    # Añadir encabezados
    headers = [
        'Nombre', 'Cantidad','unidadMedida','Descripción', 'Código CABYS', 
        'Moneda', 'Precio del Costo', 'Precio de Venta','Clasificación'
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
                producto.clasificacion or '',
                
            ])

    # Definir la respuesta HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="productos.xlsx"'

    # Guardar el archivo Excel en la respuesta
    wb.save(response)

    return response

