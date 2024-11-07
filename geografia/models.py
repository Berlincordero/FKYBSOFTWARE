#geografia/models.py
from django.db import models

class Provincia(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Canton(models.Model):
    nombre = models.CharField(max_length=100)
    provincia = models.ForeignKey(Provincia, related_name="cantones", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} ({self.provincia.nombre})"

class Distrito(models.Model):
    nombre = models.CharField(max_length=100)
    canton = models.ForeignKey(Canton, related_name="distritos", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} ({self.canton.nombre})"
