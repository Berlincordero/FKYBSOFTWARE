# Generated by Django 5.0.6 on 2024-12-29 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0004_remove_producto_descuento'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='unidad_medida',
            field=models.CharField(choices=[('Unidades', 'Unidades'), ('Kilogramos', 'Kilogramos'), ('Litros', 'Litros'), ('Metros', 'Metros'), ('Pulgadas', 'Pulgadas'), ('Galones', 'Galones'), ('Otro', 'Otro')], default='none', max_length=20),
        ),
    ]
