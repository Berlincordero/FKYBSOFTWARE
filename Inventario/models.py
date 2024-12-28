from django.db import models


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()
    descripcion = models.TextField(null=True, blank=True)
    codigo_cabys = models.CharField(max_length=20)
    moneda = models.CharField(max_length=10, choices=[('CRC', 'Colones'), ('USD', 'Dólares'), ('EUR', 'Euros')])
    precio_costo = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2) 
    clasificacion = models.CharField(max_length=50,choices=[('Materiales', 'Materiales'),('Herramientas', 'Herramientas'),('Pinturas', 'Pinturas'),('Solventes', 'Solventes'),('Maderas', 'Maderas'),('Aceros', 'Aceros'),('Plásticos', 'Plásticos'),('Otros', 'Otros')])
    activo = models.BooleanField(default=True) 
    

    def __str__(self):
        return self.nombre
    

class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()