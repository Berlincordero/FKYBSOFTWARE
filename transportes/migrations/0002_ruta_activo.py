# Generated by Django 5.0.6 on 2024-11-07 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ruta',
            name='activo',
            field=models.BooleanField(default=True),
        ),
    ]