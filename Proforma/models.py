from django.db import models
# Create your models here.

class Proforma(models.Model):
    fecha = models.DateField(auto_now_add=True)
    moneda = models.CharField(max_length=10, choices=[('CRC', 'Colones'), ('USD', 'Dólares')])
    cliente = models.CharField(max_length=100)
    codigo_actividad_economica = models.CharField(max_length=10, choices=[('regular', 'Regular'), ('especial', 'Especial' ), ('exento', 'Exento')])
    medio_pago = models.CharField(max_length=100, choices=[('efectivo', 'Efectivo'), ('tarjeta', 'Tarjeta'), ('transferencia', 'Transferencia'), ('cheque', 'Cheque'), ('deposito', 'Deposito'), ('otros', 'Otros')])
    condicion_venta = models.CharField(max_length=100, choices=[('contado', 'Contado'), ('credito', 'Crédito')])
    detalles = models.TextField()
    nota = models.TextField()
    subtotal = models.FloatField()
    descuento = models.FloatField()
    iva = models.FloatField()
    total = models.FloatField()
    activo = models.BooleanField(default=True) 

    def __str__(self):
        return self.cliente
    

class proformas(models.Model):
    Proforma = models.ForeignKey(Proforma, on_delete=models.CASCADE)
    detalles = models.TextField()
    
    
