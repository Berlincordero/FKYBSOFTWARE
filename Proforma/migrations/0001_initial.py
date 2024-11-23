# Generated by Django 5.0.6 on 2024-11-14 08:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proforma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('moneda', models.CharField(choices=[('CRC', 'Colones'), ('USD', 'Dólares')], max_length=10)),
                ('cliente', models.CharField(max_length=100)),
                ('codigo_actividad_economica', models.CharField(choices=[('regular', 'Regular'), ('especial', 'Especial'), ('exento', 'Exento')], max_length=10)),
                ('medio_pago', models.CharField(choices=[('efectivo', 'Efectivo'), ('tarjeta', 'Tarjeta'), ('transferencia', 'Transferencia'), ('cheque', 'Cheque'), ('deposito', 'Deposito'), ('otros', 'Otros')], max_length=100)),
                ('condicion_venta', models.CharField(choices=[('contado', 'Contado'), ('credito', 'Crédito')], max_length=100)),
                ('detalles', models.TextField()),
                ('nota', models.TextField()),
                ('subtotal', models.FloatField()),
                ('descuento', models.FloatField()),
                ('iva', models.FloatField()),
                ('total', models.FloatField()),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='proformas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detalles', models.TextField()),
                ('Proforma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Proforma.proforma')),
            ],
        ),
    ]