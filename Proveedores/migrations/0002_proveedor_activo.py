# Generated by Django 5.0.6 on 2024-11-11 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Proveedores', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proveedor',
            name='activo',
            field=models.BooleanField(default=True),
        ),
    ]
