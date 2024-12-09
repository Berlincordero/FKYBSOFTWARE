from django.db import models

from Proforma.models import Proforma

class CuentaPorCobrar(models.Model):
    cliente = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField()
    descripcion = models.TextField()
    estado = models.CharField(
        max_length=50,
        choices=[('Pendiente', 'Pendiente'), ('Pagado', 'Pagado')],
        default='Pendiente'
    )

    def __str__(self):
        return f"{self.cliente} - {self.monto} - {self.estado}"
    
class PagoFactura(models.Model):
    numero_factura = models.CharField(max_length=20)
    monto_pago = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateField()
    metodo_pago = models.CharField(max_length=20, choices=[
        ('transferencia', 'Transferencia'),
        ('tarjeta', 'Tarjeta'),
        ('efectivo', 'Efectivo'),
        ('sinpe', 'Sinpe')
    ])

    def __str__(self):
        return f"{self.numero_factura} - {self.monto_pago}"
    
    
# En Reportes.models
class DetalleProforma(models.Model):
    proforma = models.ForeignKey(Proforma, on_delete=models.CASCADE, related_name='detalle_proformas')
    producto = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.FloatField()
    descuento = models.FloatField(default=0.0)
    total = models.FloatField()

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario - self.descuento