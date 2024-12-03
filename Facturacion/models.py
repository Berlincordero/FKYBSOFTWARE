from django.db import models

class Factura(models.Model):
    numero_factura = models.CharField(max_length=50, unique=True)
    cliente = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.DateTimeField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50)
    observaciones = models.TextField(blank=True, null=True)
    caja = models.CharField(max_length=50)  # Ej. "Caja Registradora 1"

    def __str__(self):
        return f"Factura #{self.numero_factura} - Total: {self.total}"