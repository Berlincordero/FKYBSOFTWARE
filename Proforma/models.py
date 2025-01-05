from django.db import models
import json
# Create your models here.

class Proforma(models.Model):
    fecha = models.DateField(auto_now_add=True)
    moneda = models.CharField(max_length=10, choices=[('CRC', 'Colones'), ('USD', 'Dólares')])
    cliente = models.CharField(max_length=100)
    tipo_identificacion = models.CharField(max_length=10, null=True, blank=True)  # Nuevo campo
    regimen = models.CharField(max_length=100, null=True, blank=True)  # Nuevo campo
    situacion = models.CharField(max_length=100, null=True, blank=True)  # Nuevo campo
    codigo_actividad_economica = models.CharField(max_length=10, choices=[('regular', 'Regular'), ('especial', 'Especial' ), ('exento', 'Exento')])
    medio_pago = models.CharField(max_length=100, choices=[('efectivo', 'Efectivo'), ('tarjeta', 'Tarjeta'), ('transferencia', 'Transferencia'), 
                                                           ('cheque', 'Cheque'), ('deposito', 'Deposito'), ('otros', 'Otros')])
    condicion_venta = models.CharField(max_length=100, choices=[('contado', 'Contado'), ('credito', 'Crédito')])
    detalles = models.TextField(null=True, blank=True)
    nota = models.TextField(null=True, blank=True)
    subtotal = models.FloatField()
    descuento = models.FloatField()
    iva = models.FloatField()
    total = models.FloatField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Proforma de {self.cliente} - {self.fecha}"

  # Para mostrar detalles en JSON y usarlos en el "data-line-items"
    def get_detalles_json(self):
        detalles = self.detalle_proformas_proforma.all()
        lista = []
        for d in detalles:
            lista.append({
                "producto": d.producto,  # Aquí guardamos el NOMBRE
                "descripcion": d.descripcion or "",
                "cantidad": d.cantidad,
                "precio_unitario": d.precio_unitario,
                # 'descuento' se guarda como monto colones
                "descuento": d.descuento,
                "total": d.total
            })
        return json.dumps(lista)


class DetalleProforma(models.Model):
    proforma = models.ForeignKey(
        Proforma,
        on_delete=models.CASCADE,
        related_name='detalle_proformas_proforma'
    )
    producto = models.CharField(max_length=100)  # Nombre del producto
    descripcion = models.TextField(null=True, blank=True)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.FloatField()
    descuento = models.FloatField(default=0.0)  # Monto en colones
    total = models.FloatField()

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario - self.descuento
