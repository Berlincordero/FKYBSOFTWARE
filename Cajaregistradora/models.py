from django.db import models
from django.utils.timezone import now


class AperturaCaja(models.Model):
    cajero = models.CharField(max_length=100)
    monto_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_hora_apertura = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Apertura de caja por {self.cajero} el {self.fecha_hora_apertura}"

class Factura(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    numero_factura = models.CharField(max_length=50, unique=True, blank=True)
    cliente = models.CharField(max_length=100, blank=True, null=True)
    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado_factura = models.CharField(
        max_length=50,
        choices=[('Pagada', 'Pagada'), ('Pendiente', 'Pendiente')],
        default='Pendiente'
    )
    tipo_pago = models.CharField(max_length=20, default="Efectivo")  # Nuevo campo

    def save(self, *args, **kwargs):
        if not self.numero_factura:
            # Generar un número de factura único
            last_factura = Factura.objects.last()
            new_number = 0 if not last_factura else int(last_factura.numero_factura.split()[1]) + 1
            self.numero_factura = f"F {new_number}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Factura #{self.numero_factura} - Total: {self.total}"




class MovimientoDinero(models.Model):
    TIPO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('egreso', 'Egreso'),
    ]

    tipo_movimiento = models.CharField(choices=TIPO_CHOICES, max_length=10)
    fecha_hora = models.DateTimeField()
    usuario = models.CharField(max_length=100)
    nota = models.TextField(blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.monto}"
    
    
from django.db import models

class PreCierre(models.Model):
    sucursal = models.CharField(max_length=100, null=True, blank=True, default='Desconocida')
    caja_registradora = models.CharField(max_length=100, null=True, blank=True, default='Desconocida')
    hora_apertura = models.TimeField(null=True, blank=True)
    fecha = models.DateField(null=True, blank=True)
    monto_inicial = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    cajero = models.CharField(max_length=100, null=True, blank=True, default='No disponible')
    impuestos = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    efectivo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    facturas_proveedor = models.IntegerField(null=True, blank=True, default=0)
    tarjetas = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    simpe_movil = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    venta_credito = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    movimientos = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    total_ventas = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    cantidad_facturas = models.IntegerField(null=True, blank=True, default=0)
    conteo_efectivo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    conteo_tarjetas = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    contado_efectivo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    contado_tarjetas = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)

    def __str__(self):
        return f"PreCierre - {self.sucursal} - {self.fecha}"
