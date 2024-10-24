# Generated by Django 5.0.6 on 2024-10-17 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orden_de_compra', '0003_remove_ordendecompra_descuento'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordendecompra',
            name='descuento',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Descuento aplicado a la orden en %', max_digits=5),
        ),
    ]