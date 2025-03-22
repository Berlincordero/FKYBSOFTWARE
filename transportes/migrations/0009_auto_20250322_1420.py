from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('transportes', '0008_conductor_telefono'),  # Reemplaza con la migración anterior
    ]

    operations = [
        migrations.AlterField(
            model_name='ruta',
            name='nombre_conductor',
            field=models.ForeignKey(
                to='transportes.Conductor',
                on_delete=models.CASCADE,
                to_field='id_conductor',  # Asegúrate de que apunte al campo correcto
            ),
        ),
    ]