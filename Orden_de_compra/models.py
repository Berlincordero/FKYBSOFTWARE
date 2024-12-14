from django.db import models
from django.apps import apps  # Import diferido para romper el ciclo
from django.contrib.auth.models import User

class OrdenDeCompra(models.Model):
    id_orden = models.AutoField(primary_key=True) 
    usuario = models.CharField(max_length=255, unique=True)
    producto = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(help_text='Descripción del producto')
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_orden = models.DateField(auto_now_add=True)
    proveedor = models.ForeignKey(
        'Proveedores.Proveedor',  # Referencia a Proveedor usando el formato 'app.Modelo'
        on_delete=models.CASCADE
    )
    notas = models.TextField(max_length=300)
    metodo_pago = models.CharField(max_length=20, default='EFECTIVO')  # Podrías omitir choices si no los usas
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Cantidad * Precio unitario'
    )
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Orden de Compra {self.id_orden} - {self.producto}"