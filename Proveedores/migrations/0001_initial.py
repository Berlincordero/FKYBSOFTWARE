# Generated by Django 5.0.6 on 2024-10-16 00:01

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id_proveedor', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_ingreso', models.DateField(default=django.utils.timezone.now)),
                ('nombre_empresa', models.CharField(max_length=255)),
                ('tipo_identificacion', models.CharField(choices=[('JURIDICA', 'Cédula Jurídica'), ('FISICA', 'Cédula Física'), ('OTROS', 'Otros')], default='FISICA', max_length=10)),
                ('identificacion', models.CharField(max_length=50)),
                ('nombre', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('provincia', models.CharField(max_length=100)),
                ('canton', models.CharField(max_length=100)),
                ('distrito', models.CharField(max_length=100)),
                ('direccion_exacta', models.TextField(default='direccion', max_length=255)),
                ('telefono1', models.CharField(max_length=20)),
                ('telefono2', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
    ]
