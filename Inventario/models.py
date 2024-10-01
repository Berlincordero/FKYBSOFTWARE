from django.db import models

from django.db import models

# Modelo para el Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del producto
    cantidad = models.PositiveIntegerField()  # Cantidad en inventario
    unidad_medida = models.CharField(max_length=50)  # Unidad de medida (e.g., litros, kilos)
    descripcion = models.TextField(null=True, blank=True)  # Descripción del producto
    codigo_cabys = models.CharField(max_length=20)  # Código CABYS
    moneda = models.CharField(max_length=10, choices=[('CRC', 'Colones'), ('USD', 'Dólares')])  # Moneda (CRC/USD)
    precio_costo = models.DecimalField(max_digits=10, decimal_places=2)  # Precio de costo
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)  # Precio de venta
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Descuento (en %)
    clasificacion = models.CharField(max_length=50)  # Clasificación del producto (e.g., categoría)
    impuesto = models.CharField(max_length=20, choices=[('Exento', 'Exento'), ('Gravado', 'Gravado')])  # Impuesto
    inventario_seguimiento = models.BooleanField(default=False)  # Si el producto tiene seguimiento de inventario
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)  # Imagen del producto

    def __str__(self):
        return self.nombre

# Modelo para el seguimiento de inventarios
class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='movimientos_inventario')  # Producto relacionado
    fecha = models.DateTimeField(auto_now_add=True)  # Fecha del movimiento
    tipo_movimiento = models.CharField(max_length=50, choices=[('Ingreso', 'Ingreso'), ('Salida', 'Salida')])  # Tipo de movimiento
    cantidad = models.PositiveIntegerField()  # Cantidad del movimiento
    comentario = models.TextField(null=True, blank=True)  # Comentarios adicionales sobre el movimiento

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.producto.nombre} - {self.cantidad}"
