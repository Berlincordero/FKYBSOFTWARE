from django.db import models



class Factura(models.Model):
    fecha = models.DateTimeField()
    numero_factura = models.CharField(max_length=50, unique=True)
    cliente = models.CharField(max_length=100, blank=True, null=True)
    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Factura #{self.numero_factura} - Total: {self.total}"
    
    

    
    