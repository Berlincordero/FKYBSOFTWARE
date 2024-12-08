# Generated by Django 5.0.6 on 2024-12-08 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cajaregistradora', '0003_factura_estado_factura_factura_tipo_pago'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistroCaja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('hora_apertura', models.TimeField()),
                ('hora_cierre', models.TimeField(blank=True, null=True)),
                ('monto_inicial', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_calculado', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total_real', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('diferencia', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('usuario', models.CharField(max_length=255)),
            ],
        ),
    ]
