# Generated by Django 5.0.6 on 2024-12-29 08:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0006_alter_producto_unidad_medida'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventario',
            name='cantidad',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='inventario',
            name='producto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Inventario.producto'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='activo',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='cantidad',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='clasificacion',
            field=models.CharField(blank=True, choices=[('Materiales', 'Materiales'), ('Herramientas', 'Herramientas'), ('Pinturas', 'Pinturas'), ('Solventes', 'Solventes'), ('Maderas', 'Maderas'), ('Aceros', 'Aceros'), ('Plásticos', 'Plásticos'), ('Otros', 'Otros')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='codigo_cabys',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='moneda',
            field=models.CharField(blank=True, choices=[('CRC', 'Colones'), ('USD', 'Dólares'), ('EUR', 'Euros')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='nombre',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='precio_costo',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='precio_venta',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='unidad_medida',
            field=models.CharField(blank=True, choices=[('Unidades', 'Unidades'), ('Kilogramos', 'Kilogramos'), ('Litros', 'Litros'), ('Metros', 'Metros'), ('Pulgadas', 'Pulgadas'), ('Galones', 'Galones'), ('Otro', 'Otro')], max_length=20, null=True),
        ),
    ]
