# forms.py

from django import forms
from .models import Conductor, PlacaDeVehiculo, Ruta

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=200)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class ConductorForm(forms.Form):
    cedula = forms.CharField(label='Cédula', max_length=20)
    nombre = forms.CharField(label='Nombre', max_length=100)
    apellidos = forms.CharField(label='Apellidos', max_length=100)

class PlacaDeVehiculoForm(forms.Form):
    placa = forms.CharField(label='Número de Placa', max_length=10)

class RutaForm(forms.Form):
    nombre_ruta = forms.CharField(label='Nombre de la Ruta', max_length=100)
    numero_factura = forms.CharField(label='Número de Factura', max_length=20)

class MiFormulario(forms.Form):
    # Define los campos que necesitas
    campo1 = forms.CharField(max_length=100)
    campo2 = forms.EmailField()
    # Agrega más campos según sea necesario
