# config/models.py

from django.db import models

class Conductor(models.Model):
    cedula = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    apellido1 = models.CharField(max_length=100)
    apellido2 = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido1} {self.apellido2}"

class PlacaDeVehiculo(models.Model):
    conductor = models.ForeignKey(Conductor, on_delete=models.CASCADE)
    numero_placa = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.numero_placa

class Ruta(models.Model):
    conductor = models.ForeignKey(Conductor, on_delete=models.CASCADE)
    placa = models.ForeignKey(PlacaDeVehiculo, on_delete=models.CASCADE)
    nombre_ruta = models.CharField(max_length=100)
    numero_factura = models.CharField(max_length=50)
    hora_salida = models.TimeField()

    def __str__(self):
        return f"Ruta {self.nombre_ruta} - {self.numero_factura}"
    
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