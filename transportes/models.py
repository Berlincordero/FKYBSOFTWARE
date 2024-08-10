from django.db import models

class Conductor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido1 = models.CharField(max_length=100)
    apellido2 = models.CharField(max_length=100, blank=True)
    cedula = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido1} {self.apellido2}"

class Vehiculo(models.Model):
    numero_placa = models.CharField(max_length=20, unique=True)
    conductor = models.ForeignKey(Conductor, on_delete=models.CASCADE)

    def __str__(self):
        return self.numero_placa

class Ruta(models.Model):
    numero_factura = models.CharField(max_length=20)
    provincia = models.CharField(max_length=100)
    canton = models.CharField(max_length=100)
    distrito = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Ruta {self.numero_factura} - {self.direccion}"
