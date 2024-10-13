# Generated by Django 5.0.6 on 2024-10-13 05:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('cantidad', models.PositiveIntegerField()),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('codigo_cabys', models.CharField(max_length=20)),
                ('moneda', models.CharField(choices=[('CRC', 'Colones'), ('USD', 'Dólares')], max_length=10)),
                ('precio_costo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('precio_venta', models.DecimalField(decimal_places=2, max_digits=10)),
                ('descuento', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('clasificacion', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inventario.producto')),
            ],
        ),
    ]
