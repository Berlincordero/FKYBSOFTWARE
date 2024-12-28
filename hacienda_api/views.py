from django.shortcuts import render
import requests
# Create your views here.
# hacienda_api/views.py
from django.http import JsonResponse
from .service import consultar_hacienda

def buscar_cliente(request):
    """
    Vista que recibe un parámetro 'cedula' por querystring 
    y llama a la API de Hacienda para obtener los datos.
    """
    cedula = request.GET.get('cedula', None)
    if not cedula:
        return JsonResponse({
            "success": False,
            "error": "No se ha proporcionado la cédula."
        }, status=400)

    # Llama a la API pública de Hacienda
    url = f"https://api.hacienda.go.cr/fe/ae?identificacion={cedula}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()

            # Extrae los datos necesarios
            nombre = data.get('nombre', '')
            tipo_identificacion = data.get('tipoIdentificacion', '')
            regimen = data.get('regimen', {}).get('descripcion', '')
            situacion = data.get('situacion', {}).get('estado', '')

            return JsonResponse({
                "success": True,
                "nombre": nombre,
                "tipo_identificacion": tipo_identificacion,
                "regimen": regimen,
                "situacion": situacion
            })
        else:
            return JsonResponse({
                "success": False,
                "error": f"Error al consultar Hacienda: {response.status_code}"
            })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": f"Error al conectar con Hacienda: {str(e)}"
        })