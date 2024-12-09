# Generated by Django 5.0.6 on 2024-12-08 19:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Proforma", "0006_alter_detalleproforma_proforma"),
        ("Reportes", "0003_detalleproforma"),
    ]

    operations = [
        migrations.AlterField(
            model_name="detalleproforma",
            name="proforma",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="detalle_proformas",
                to="Proforma.proforma",
            ),
        ),
    ]
