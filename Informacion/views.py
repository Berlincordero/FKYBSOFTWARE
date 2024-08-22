from django.shortcuts import render

# Create your views here.

def informacion_view(request):
    return render(request, 'informacion.html')