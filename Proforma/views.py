from django.shortcuts import render

# Create your views here.


def proforma_view(request):
    return render(request, 'Proforma.html')



