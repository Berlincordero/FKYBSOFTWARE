# Generated by Django 5.0.6 on 2025-01-29 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportes', '0007_vehiculo_activo_vehiculoeliminado'),
    ]

    operations = [
        migrations.AddField(
            model_name='conductor',
            name='telefono',
            field=models.CharField(default=1, max_length=15),
            preserve_default=False,
        ),
    ]
