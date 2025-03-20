from django.db import models


class Producto(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True)
    cantidad = models.PositiveIntegerField(null=True, blank=True)
    unidad_medida = models.CharField(
        max_length=20,
        choices=[
            ('Unidades', 'Unidades'),
            ('Kilogramos', 'Kilogramos'),
            ('Gramos', 'Gramos'),
            ('Litros', 'Litros'),
            ('Metros', 'Metros'),
            ('Pulgadas', 'Pulgadas'),
            ('Galones', 'Galones'),
            ('Otro', 'Otro'),
        ],
        null=True,
        blank=True
    )
    descripcion = models.TextField(null=True, blank=True)
    codigo_cabys = models.CharField(max_length=20, null=True, blank=True, unique=True)
    moneda = models.CharField(
        max_length=10,
        choices=[
            ('CRC', 'Colones'),
            ('USD', 'Dólares'),
            ('EUR', 'Euros'),
        ],
        null=True,
        blank=True
    )
    precio_costo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    clasificacion = models.CharField(
        max_length=50,
        choices=[
            ('Materiales', 'Materiales'),
            ('Herramientas', 'Herramientas'),
            ('Pinturas', 'Pinturas'),
            ('Solventes', 'Solventes'),
            ('Maderas', 'Maderas'),
            ('Aceros', 'Aceros'),
            ('Plásticos', 'Plásticos'),
            ('Otros', 'Otros'),
        ],
        null=True,
        blank=True
    )
    activo = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return self.nombre if self.nombre else "Producto sin nombre"


class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.PositiveIntegerField(null=True, blank=True)
