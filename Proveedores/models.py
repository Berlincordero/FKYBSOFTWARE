from django.db import models
from django.utils import timezone

class Proveedor(models.Model):
    codigo = models.CharField(max_length=100, default='DEFAULT_VALUE')
    fecha = models.DateTimeField(default=timezone.now)
    nombreempresa = models.CharField(max_length=100)
    tipoIdentificacion = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    provincia = models.CharField(max_length=100)
    canton = models.CharField(max_length=100)
    distrito = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono1 = models.CharField(max_length=100)
    telefono2 = models.CharField(max_length=100)
  
    def __str__(self):
        return self.nombre