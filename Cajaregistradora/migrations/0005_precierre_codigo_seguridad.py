# Generated by Django 5.0.6 on 2024-12-19 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cajaregistradora', '0004_movimientodinero_codigo_seguridad'),
    ]

    operations = [
        migrations.AddField(
            model_name='precierre',
            name='codigo_seguridad',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
