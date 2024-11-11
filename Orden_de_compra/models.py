from django.db import models

class OrdenDeCompra(models.Model):
    id_orden = models.AutoField(primary_key=True) 
    id_usuario = models.CharField(max_length=255, unique=True)
    id_proveedor = models.CharField(max_length=255, unique=True)
    id_producto = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(help_text='Descripción del producto')
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_orden = models.DateField(auto_now_add=True)
    proveedor = models.CharField(max_length=255)
    descuento = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text='Descuento aplicado a la orden de compra'
    )
    lugar_entrega = models.TextField(max_length=300)
    notas = models.TextField(max_length=300)
    metodo_pago = models.CharField(max_length=20, default='EFECTIVO')  # Podrías omitir choices si no los usas
    IVI = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=13.00,
        help_text='Porcentaje del IVA'
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Subtotal de la orden de compra'
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Total después de aplicar descuento e IVA'
    )
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Orden de Compra {self.id_orden} - {self.id_producto}"