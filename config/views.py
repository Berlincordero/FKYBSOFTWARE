from django.shortcuts import render

def index(request):
    return render(request, 'base.html')

def pos_view(request):
    return render(request, 'Terminal.html')

def base2(request):
    return render(request, 'base2.html')

