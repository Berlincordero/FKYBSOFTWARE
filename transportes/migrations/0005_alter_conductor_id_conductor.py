# Generated by Django 5.0.6 on 2024-12-15 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportes', '0004_remove_conductor_id_alter_conductor_id_conductor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conductor',
            name='id_conductor',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]