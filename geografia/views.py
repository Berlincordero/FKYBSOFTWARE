#geografia/views.py
import csv
from django.shortcuts import render
from django.http import HttpResponse
from .models import Provincia, Canton, Distrito
from django.http import JsonResponse

def cargar_datos(request):
    if request.method == 'POST' and request.FILES['archivo']:
        archivo = request.FILES['archivo']
        reader = csv.DictReader(archivo.read().decode('utf-8').splitlines())
        
        for row in reader:
            provincia, created = Provincia.objects.get_or_create(nombre=row['provincia'])
            canton, created = Canton.objects.get_or_create(nombre=row['canton'], provincia=provincia)
            Distrito.objects.get_or_create(nombre=row['distrito'], canton=canton)

        return HttpResponse("Datos cargados con éxito!")
    
    return render(request, 'geografia/cargar_datos.html')

# Obtener cantones según la provincia seleccionada
def obtener_cantones(request, provincia_id):
    cantones = Canton.objects.filter(provincia_id=provincia_id)
    canton_data = [{"id": canton.id, "nombre": canton.nombre} for canton in cantones]
    return JsonResponse({"cantones": canton_data})

# Obtener distritos según el cantón seleccionado
def obtener_distritos(request, canton_id):
    distritos = Distrito.objects.filter(canton_id=canton_id)
    distrito_data = [{"id": distrito.id, "nombre": distrito.nombre} for distrito in distritos]
    return JsonResponse({"distritos": distrito_data})