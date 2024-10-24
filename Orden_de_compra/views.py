# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from Proveedores.models import Proveedor
from Inventario.models import Producto
from .models import OrdenDeCompra
from .forms import OrdenDeCompraForm


def orden_de_compra(request):
    productos = Producto.objects.all()
    proveedores = Proveedor.objects.all()
    orden_de_compra  = OrdenDeCompra.objects.all()
    return render(request, 'ordenes/orden_de_compra.html', {'orden_de_compra ': orden_de_compra, 'productos': productos})

def agregar_orden(request):
    if request.method == 'POST':
        id_proveedor = request.POST.get('id_proveedor')
        id_producto = request.POST.get('id_producto')
        descripcion = request.POST.get('descripcion')
        cantidad = int(request.POST.get('cantidad', 0))
        precio_unitario = float(request.POST.get('precio_unitario', 0.0))
        lugar_entrega = request.POST.get('direccion')
        notas = request.POST.get('nota','Sin notas')
        metodo_pago = request.POST.get('metodo_pago')

        """usuario = get_object_or_404(User, pk=id_usuario)"""
        usuario = User.objects.get(username="admin")
        proveedor_obj = get_object_or_404(Proveedor, pk=id_proveedor) if id_proveedor else None

        if not proveedor_obj:
            # En caso de que el proveedor no se encuentre, puedes asignar un proveedor predeterminado aquí
            proveedor_obj = Proveedor.objects.first()  # o asigna el primer proveedor en la base de datos

        producto_obj = get_object_or_404(Producto, pk=id_producto)

        OrdenDeCompra.objects.create(
            id_usuario=usuario,
            id_proveedor=proveedor_obj,
            id_producto=producto_obj,
            descripcion=descripcion,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            lugar_entrega=lugar_entrega,
            notas=notas,
            metodo_pago=metodo_pago
        )

        return redirect('orden_de_compra')

    usuarios = User.objects.all()
    proveedores = Proveedor.objects.all()
    productos = Producto.objects.all()
    return render(request, 'orden_de_compra/agregar_orden.html', {
        'usuarios': usuarios,
        'proveedores': proveedores,
        'productos': productos
    })
    