# transportes/models.py


#Conductores
from django.db import models

class Conductor(models.Model):
    id_conductor = models.CharField(max_length=50,primary_key=True)
    nombre_conductor = models.CharField(max_length=100)
    apellidos_1 = models.CharField(max_length=100)
    apellidos_2 = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=15) # 29/01/2025
    activo = models.BooleanField(default=True)  # Campo para marcar rutas activas o no

    def __str__(self):
        return f"{self.nombre_conductor} {self.apellidos_1} {self.apellidos_2}"
       
    
class ConductorEliminado(models.Model):
    conductor = models.ForeignKey(Conductor, on_delete=models.CASCADE)
    fecha_eliminacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Conductor {self.conductor.id_conductor} eliminada el {self.fecha_eliminacion}" 
        
    
    
#class ConductorEliminado(models.Model):
    #conductor = models.ForeignKey(Conductor, on_delete=models.CASCADE)
    #fecha_eliminacion = models.DateTimeField(auto_now_add=True)

    #def __str__(self):
        #return f"{self.conductor.nombre_conductor} {self.conductor.apellidos_1} {self.conductor.apellidos_2} - Eliminado en: {self.fecha_eliminacion}"
    
    
# Vehiculos    
    
class Vehiculo(models.Model):
    id_vehiculo = models.CharField(max_length=20, primary_key=True)  # Cambiado a CharField
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    año = models.IntegerField()
    activo = models.BooleanField(default=True)  # Campo para marcar rutas activas o no

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.año})"
    
class VehiculoEliminado(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha_eliminacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Vehiculo {self.vehiculo.id_vehiculo} eliminada el {self.fecha_eliminacion}"     
    
    
# Rutas    

class Ruta(models.Model):
    id_ruta = models.CharField(max_length=50, primary_key=True)
    fecha_ruta = models.DateField()
    provincia = models.CharField(max_length=100)
    canton = models.CharField(max_length=100)
    distrito = models.CharField(max_length=100)
    direccion_exacta = models.CharField(max_length=255)
    nombre_conductor = models.ForeignKey(Conductor, on_delete=models.CASCADE)
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)  # Campo para marcar rutas activas o no

    def __str__(self):
        return f"Ruta {self.id_ruta} - {self.fecha_ruta}"



class RutaEliminada(models.Model):
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    fecha_eliminacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ruta {self.ruta.id_ruta} eliminada el {self.fecha_eliminacion}"
    
class RutaPrecio(models.Model):
    id = models.AutoField(primary_key=True)  # ID
    ruta = models.ForeignKey(Ruta, to_field='id_ruta', on_delete=models.CASCADE)  # Relación con id_ruta de Ruta
    precio_ruta = models.DecimalField(max_digits=10, decimal_places=2, choices=[(5000, '5000'), (10000, '10000')])  # Precio
    kilometro = models.IntegerField(choices=[(1, '1'), (2, '2')])  # Kilómetros

    def __str__(self):
        return f"Ruta {self.ruta.id_ruta} - Precio: {self.precio_ruta} - Km: {self.kilometro}"






  