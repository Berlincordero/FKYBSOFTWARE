# Generated by Django 5.0.6 on 2024-10-26 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="OrdenDeCompra",
            fields=[
                ("id_orden", models.AutoField(primary_key=True, serialize=False)),
                ("id_usuario", models.CharField(max_length=255, unique=True)),
                ("id_proveedor", models.CharField(max_length=255, unique=True)),
                ("id_producto", models.CharField(max_length=255, unique=True)),
                ("descripcion", models.TextField(help_text="Descripción del producto")),
                ("cantidad", models.PositiveIntegerField()),
                (
                    "precio_unitario",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("fecha_orden", models.DateField(auto_now_add=True)),
                ("proveedor", models.CharField(max_length=255)),
                (
                    "descuento",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        help_text="Descuento aplicado a la orden de compra",
                        max_digits=5,
                    ),
                ),
                ("lugar_entrega", models.TextField(max_length=300)),
                ("notas", models.TextField(max_length=300)),
                ("metodo_pago", models.CharField(default="EFECTIVO", max_length=20)),
                (
                    "IVI",
                    models.DecimalField(
                        decimal_places=2,
                        default=13.0,
                        help_text="Porcentaje del IVA",
                        max_digits=5,
                    ),
                ),
                (
                    "subtotal",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        help_text="Subtotal de la orden de compra",
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "total",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        help_text="Total después de aplicar descuento e IVA",
                        max_digits=10,
                        null=True,
                    ),
                ),
            ],
        ),
    ]
