# transportes/admin.py
from django.contrib import admin
from .models import Conductor, Vehiculo, Ruta, RutaEliminada


admin.site.register(Conductor)
admin.site.register(Vehiculo)
admin.site.register(Ruta)
admin.site.register(RutaEliminada)