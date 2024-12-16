# transportes/admin.py
from django.contrib import admin
from .models import Conductor, Vehiculo, Ruta, RutaEliminada, ConductorEliminado, VehiculoEliminado


admin.site.register(Conductor)
admin.site.register(ConductorEliminado)
admin.site.register(Vehiculo)
admin.site.register(VehiculoEliminado)
admin.site.register(Ruta)
admin.site.register(RutaEliminada)