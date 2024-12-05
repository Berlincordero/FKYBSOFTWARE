from django.db import models

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

    def save(self, *args, **kwargs):
        if not self.numero_factura:
            # Obtiene la última factura para determinar el número siguiente
            last_factura = Factura.objects.last()
            new_number = 0 if not last_factura else int(last_factura.numero_factura.split()[1]) + 1
            self.numero_factura = f"F {new_number}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Factura #{self.numero_factura} - Total: {self.total}"
    
    