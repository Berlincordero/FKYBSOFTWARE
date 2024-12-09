from django.db import models
from django.utils.timezone import now

class RegistroCaja(models.Model):
    fecha = models.DateField(auto_now_add=True)  # Fecha en que se abre la caja
    hora_apertura = models.TimeField(auto_now_add=True)  # Hora exacta de apertura
    monto_inicial = models.DecimalField(max_digits=10, decimal_places=2)  # Monto inicial ingresado
    usuario = models.CharField(max_length=255)  # Nombre o ID del usuario que abre la caja
    estado = models.CharField(
        max_length=10,
        choices=[('Abierta', 'Abierta'), ('Cerrada', 'Cerrada')],
        default='Abierta'
    )

    def __str__(self):
        return f"Caja abierta por {self.usuario} el {self.fecha} a las {self.hora_apertura}"


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


