# Generated by Django 5.0.6 on 2024-10-17 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orden_de_compra', '0005_alter_ordendecompra_ivi_alter_ordendecompra_subtotal_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordendecompra',
            name='notas',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
    ]
