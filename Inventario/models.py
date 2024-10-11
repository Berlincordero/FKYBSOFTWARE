from django.db import models


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()
    descripcion = models.TextField(null=True, blank=True)
    codigo_cabys = models.CharField(max_length=20)
    moneda = models.CharField(max_length=10, choices=[('CRC', 'Colones'), ('USD', 'Dólares')])
    precio_costo = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    clasificacion = models.CharField(max_length=50)


    def __str__(self):
        return self.nombre
    

class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()