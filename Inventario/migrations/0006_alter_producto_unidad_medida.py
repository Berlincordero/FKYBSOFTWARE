# Generated by Django 5.0.6 on 2024-12-29 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0005_producto_unidad_medida'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='unidad_medida',
            field=models.CharField(choices=[('Unidades', 'Unidades'), ('Kilogramos', 'Kilogramos'), ('Litros', 'Litros'), ('Metros', 'Metros'), ('Pulgadas', 'Pulgadas'), ('Galones', 'Galones'), ('Otro', 'Otro')], max_length=20),
        ),
    ]
