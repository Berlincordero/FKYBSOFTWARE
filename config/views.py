from django.shortcuts import render

def index(request):
    return render(request, 'base.html')

def pos_view(request):
    return render(request, 'pos_template.html')
