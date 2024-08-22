from django.shortcuts import render, redirect

def index(request):
    return render(request, 'index.html')



def modulo_transportes(request):
    return render(request, 'modulo_transportes.html')

