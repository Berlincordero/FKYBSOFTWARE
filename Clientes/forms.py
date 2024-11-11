from django import forms
from .models import Cliente
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['id_cliente', 'nombre', 'primer_apellido', 'segundo_apellido', 'provincia', 'canton', 'distrito', 'direccion_exacta', 'telefono', 'correo']