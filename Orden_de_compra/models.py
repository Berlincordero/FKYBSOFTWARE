# Create your models here.
from django.db import models


class OrdenDeCompra(models.Model):
    # Opciones para el campo de descuento
    DESCUENTO_CHOICES = [
        (5, '5%'),
        (10, '10%'),
        (15, '15%'),
        (20, '20%'),
        (30, '30%'),
    ]
    PAGO_CHOICES = [
        ('EFECTIVO', 'efectivo'),
        ('TRANSFERENCIA', 'transferencia'),
        ('LETRA_DE_CAMBIO', 'letra_de_cambio'),
        ('SINPE', 'sinpe'),
        ('OTROS', 'otros'),
    ]
    id_orden = models.CharField(max_length=255, unique=True)
    id_usuario = models.CharField(max_length=255, unique=True)
    id_proveedor = models.CharField(max_length=255, unique=True)
    id_producto = models.CharField(max_length=255, unique=True)  # Cambiado de 'producto' a 'id_producto'
    descripcion = models.TextField(help_text='Descripción del producto')
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_orden = models.DateField(auto_now_add=True)
    proveedor = models.CharField(max_length=255)
    descuento = models.PositiveIntegerField(
        choices=DESCUENTO_CHOICES,
        default=5,
        help_text='Descuento aplicado a la orden de compra'
    )
    lugar_entrega = models.TextField(max_length=300)
    notas = models.TextField(max_length=300)
    metodo_pago = models.CharField(max_length=20, choices= PAGO_CHOICES, default='')
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

    def save(self, *args, **kwargs):
        # Calcular el subtotal y total antes de guardar el modelo
        self.subtotal = self.cantidad * self.precio_unitario
        total_descuento = self.subtotal * (self.descuento / 100)
        subtotal_con_descuento = self.subtotal - total_descuento
        total_iva = subtotal_con_descuento * (self.IVI / 100)
        self.total = subtotal_con_descuento + total_iva
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Orden de Compra {self.id} - {self.id_producto}"

