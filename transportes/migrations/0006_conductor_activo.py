# Generated by Django 5.0.6 on 2024-12-15 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportes', '0005_alter_conductor_id_conductor'),
    ]

    operations = [
        migrations.AddField(
            model_name='conductor',
            name='activo',
            field=models.BooleanField(default=True),
        ),
    ]
