# clientes/models.py
from django.db import models

class Cliente(models.Model):
    id_cliente = models.CharField(primary_key=True, max_length=20)  # Cambiar a CharField
    nombre = models.CharField(max_length=100)
    primer_apellido = models.CharField(max_length=100)
    segundo_apellido = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    canton = models.CharField(max_length=100)
    distrito = models.CharField(max_length=100)
    direccion_exacta = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField(max_length=100)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.primer_apellido} {self.segundo_apellido}"

class ClienteEliminado(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_eliminacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cliente {self.cliente.id_cliente} eliminado el {self.fecha_eliminacion}"
