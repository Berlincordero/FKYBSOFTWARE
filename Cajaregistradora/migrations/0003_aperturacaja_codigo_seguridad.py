# Generated by Django 5.0.6 on 2024-12-18 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cajaregistradora', '0002_aperturacaja_fecha_hora_cierre'),
    ]

    operations = [
        migrations.AddField(
            model_name='aperturacaja',
            name='codigo_seguridad',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
