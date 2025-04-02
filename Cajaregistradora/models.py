from django.db import models
from django.utils.timezone import now


class AperturaCaja(models.Model):
    cajero = models.CharField(max_length=100)
    monto_inicial = models.DecimalField(max_digits=100, decimal_places=2)
    fecha_hora_apertura = models.DateTimeField(auto_now_add=True)
    abierta = models.BooleanField(default=True)  # Campo existente para el estado de la caja
    fecha_hora_cierre = models.DateTimeField(null=True, blank=True)  # Nuevo campo para la hora de cierre
    codigo_seguridad = models.CharField(max_length=100, null=True, blank=True)  # Nuevo campo para el código de seguridad

    def __str__(self):
        return f"Apertura de caja por {self.cajero} el {self.fecha_hora_apertura}"

class Factura(models.Model):
    apertura_caja = models.ForeignKey(AperturaCaja, on_delete=models.SET_NULL, null=True, blank=True, related_name='facturas')
    fecha = models.DateTimeField(auto_now_add=True)
    numero_factura = models.CharField(max_length=100, blank=True)
    cliente = models.CharField(max_length=100, blank=True, null=True)
    tipo_identificacion = models.CharField(max_length=10, blank=True, null=True)
    regimen = models.CharField(max_length=100, blank=True, null=True)
    situacion_tributaria = models.CharField(max_length=100, blank=True, null=True)
    codigo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    precio_venta = models.DecimalField(max_digits=100, decimal_places=2)
    iva = models.DecimalField(max_digits=100, decimal_places=2)
    total = models.DecimalField(max_digits=100, decimal_places=2)
    estado_factura = models.CharField(
        max_length=100,
        choices=[('Pagada', 'Pagada'), ('Pendiente', 'Pendiente')],
        default='Pendiente'
    )
    metodo_pago = models.CharField(max_length=100, default="cash")  # valores: cash, creditCard, simpeMovil, credit, transfer
    tipo_precio = models.CharField(max_length=100, default="Regular") # Regular, Mayorista, Proveedor

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
    apertura_caja = models.ForeignKey(AperturaCaja, on_delete=models.SET_NULL, null=True, blank=True, related_name='movimientos')
    TIPO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('egreso', 'Egreso'),
    ]
    tipo_movimiento = models.CharField(choices=TIPO_CHOICES, max_length=10)
    fecha_hora = models.DateTimeField()
    usuario = models.CharField(max_length=100)
    nota = models.TextField(blank=True, null=True)
    monto = models.DecimalField(max_digits=1000, decimal_places=2)
    codigo_seguridad = models.CharField(max_length=50, null=True, blank=True)  # Nuevo campo

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.monto}"
# Cajaregistradora/models.py
class PreCierre(models.Model):
    apertura_caja = models.OneToOneField(AperturaCaja, on_delete=models.CASCADE, related_name='precierre')
    sucursal = models.CharField(max_length=100, null=True, blank=True, default='Desconocida')
    caja_registradora = models.CharField(max_length=100, null=True, blank=True, default='Desconocida')
    hora_apertura = models.TimeField(null=True, blank=True)
    fecha = models.DateField(null=True, blank=True)
    monto_inicial = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    cajero = models.CharField(max_length=100, null=True, blank=True, default='No disponible')
    impuestos = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True, default=0.00)
    efectivo = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True, default=0.00)
    facturas_proveedor = models.IntegerField(null=True, blank=True, default=0)
    tarjetas = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True, default=0.00)
    simpe_movil = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True, default=0.00)
    venta_credito = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True, default=0.00)
    movimientos = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True, default=0.00)
    total_ventas = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True, default=0.00)
    cantidad_facturas = models.IntegerField(null=True, blank=True, default=0)
    conteo_efectivo = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True, default=0.00)
    conteo_tarjetas = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True, default=0.00)
    contado_efectivo = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True, default=0.00)
    contado_tarjetas = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True, default=0.00)
    codigo_seguridad = models.CharField(max_length=50, null=True, blank=True)  # Agregado

    def __str__(self):
        return f"PreCierre - {self.sucursal} - {self.fecha}"

# Este Codigo tiene copyrights 2024  estructurado por Berlin Cordero Brenes