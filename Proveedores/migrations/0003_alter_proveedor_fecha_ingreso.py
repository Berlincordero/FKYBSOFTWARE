# Generated by Django 5.0.6 on 2024-12-13 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Proveedores', '0002_proveedor_activo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedor',
            name='fecha_ingreso',
            field=models.DateField(auto_now_add=True),
        ),
    ]
