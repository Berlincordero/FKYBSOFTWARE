#transportes/forms.py
from django import forms
from .models import Conductor, Vehiculo, Ruta

class ConductorForm(forms.ModelForm):
    class Meta:
        model = Conductor
        fields = ['id_conductor', 'nombre_conductor', 'apellidos_1', 'apellidos_2']
        
class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['id_vehiculo', 'marca', 'modelo', 'año']        
        
        
class RutaForm(forms.ModelForm):
    class Meta:
        model = Ruta
        fields = [
            'fecha_ruta',
            'provincia',
            'canton',
            'distrito',
            'direccion_exacta',
            'nombre_conductor',
            'id_vehiculo'
        ]
        widgets = {
            'fecha_ruta': forms.DateInput(attrs={'type': 'date'}),
            'direccion_exacta': forms.TextInput(attrs={'placeholder': 'Ingrese dirección exacta'}),
            'nombre_conductor': forms.Select(),  # Esto será llenado dinámicamente
            'id_vehiculo': forms.Select(),  # Esto será llenado dinámicamente
        }

    def __init__(self, *args, **kwargs):
        conductores = kwargs.pop('conductores', None)
        vehiculos = kwargs.pop('vehiculos', None)
        super(RutaForm, self).__init__(*args, **kwargs)
        if conductores:
            self.fields['nombre_conductor'].queryset = conductores
        if vehiculos:
            self.fields['id_vehiculo'].queryset = vehiculos


