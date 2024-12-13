from django.db import models

class Proveedor(models.Model):
    CEDULA_CHOICES = [
        ('JURIDICA', 'Cédula Jurídica'),
        ('FISICA', 'Cédula Física'),
        ('OTROS', 'Otros'),
    ]
 
    id_proveedor = models.AutoField(primary_key=True)
    fecha_ingreso = models.DateField(auto_now_add=True)  
    nombre_empresa = models.CharField(max_length=255)
    tipo_identificacion = models.CharField(max_length=10, choices=CEDULA_CHOICES, default='FISICA')
    identificacion = models.CharField(max_length=50)
    nombre = models.CharField(max_length=255)
    email = models.EmailField()
    provincia = models.CharField(max_length=100)
    canton = models.CharField(max_length=100)
    distrito = models.CharField(max_length=100)
    direccion_exacta = models.TextField(default='direccion', max_length=255)
    telefono1 = models.CharField(max_length=20)
    telefono2 = models.CharField(max_length=20, blank=True, null=True)
    activo = models.BooleanField(default=True)
 
    def __str__(self):
        return self.nombre_empresa