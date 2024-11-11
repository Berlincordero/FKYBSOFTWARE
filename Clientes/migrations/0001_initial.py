# Generated by Django 5.0.6 on 2024-11-10 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id_cliente', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('primer_apellido', models.CharField(max_length=100)),
                ('segundo_apellido', models.CharField(blank=True, max_length=100)),
                ('provincia', models.CharField(max_length=100)),
                ('canton', models.CharField(max_length=100)),
                ('distrito', models.CharField(max_length=100)),
                ('direccion_exacta', models.CharField(max_length=255)),
                ('telefono', models.CharField(blank=True, max_length=15)),
                ('correo', models.EmailField(blank=True, max_length=100)),
            ],
        ),
    ]
