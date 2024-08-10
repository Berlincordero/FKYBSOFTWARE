from django.db import models

# Create your models here.


class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    cedula = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    apellido1 = models.CharField(max_length=100)
    apellido2 = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=255)
    telefono = models.CharField(max_length=20)
    provincia = models.CharField(max_length=100)
    canton = models.CharField(max_length=100)
    distrito = models.CharField(max_length=100)
    direccion = models.TextField()

    def __str__(self):
        return f"{self.nombre} {self.apellido1}"