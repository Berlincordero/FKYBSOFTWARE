from django.conf import settings
from django.shortcuts import render

# Create your views here.
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    # Ajustar para entorno local
    if ip == '127.0.0.1':
        ip = '192.168.0.101'  # IP unica de terminal local
    return ip

def Cajaregistradora_view(request):
    client_ip = get_client_ip(request)
    
     # Configuración de terminales
    TERMINAL_CONFIG = {
        'Caja Registradora 1': '192.168.0.101',
        'Caja Registradora 2': '192.168.0.102',
        # Agrega más terminales si es necesario
    }
    
    terminal = next(
        (name for name, ip in TERMINAL_CONFIG.items() if ip == client_ip),
        "Terminal Desconocida"
    )

    return render(request, 'Cajaregistradora.html', {'terminal': terminal})



