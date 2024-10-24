# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from Proveedores.models import Proveedor
from Inventario.models import Producto
from decimal import Decimal


class OrdenDeCompra(models.Model):
    # Opciones para el campo de descuento
    
    PAGO_CHOICES = [
        ('EFECTIVO', 'efectivo'),
        ('TRANSFERENCIA', 'transferencia'),
        ('LETRA_DE_CAMBIO', 'letra_de_cambio'),
        ('SINPE', 'sinpe'),
        ('OTROS', 'otros'),
    ]
    id_orden = models.CharField(max_length=255, primary_key=True)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuarios")
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, verbose_name="Proveedores")
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name="Producto")  # Cambiado de 'producto' a 'id_producto'
    descripcion = models.TextField(help_text='Descripción del producto')
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_orden = models.DateField(auto_now_add=True)
    proveedor = models.CharField(max_length=255)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text='Descuento aplicado a la orden en %')

    lugar_entrega = models.TextField(max_length=300)
    notas = models.TextField(max_length=300, blank=True, null=True)    
    metodo_pago = models.CharField(max_length=20, choices= PAGO_CHOICES, default='')
    IVI = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('13.00'))
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Cálculos asegurando que sean con Decimal
        self.subtotal = Decimal(self.cantidad) * Decimal(self.precio_unitario)
        total_descuento = self.subtotal * (Decimal(self.descuento) / Decimal(100))
        subtotal_con_descuento = self.subtotal - total_descuento
        total_iva = subtotal_con_descuento * (self.IVI / Decimal(100))
        self.total = subtotal_con_descuento + total_iva

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Orden de Compra {self.id_orden} - {self.id_proveedor.nombre_empresa}"

