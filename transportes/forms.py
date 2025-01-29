#transportes/forms.py
from django import forms
from geografia.models import Provincia, Canton, Distrito
from .models import Conductor, Vehiculo, Ruta

class ConductorForm(forms.ModelForm):
    class Meta:
        model = Conductor
        fields = ['id_conductor', 'nombre_conductor', 'apellidos_1', 'apellidos_2','telefono']
        
class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['id_vehiculo', 'marca', 'modelo', 'año']        
        
        
class RutaForm(forms.ModelForm):
    class Meta:
        model = Ruta
        fields = ['fecha_ruta', 'provincia', 'canton', 'distrito', 'direccion_exacta', 'nombre_conductor', 'id_vehiculo']

    # Widgets para las relaciones
    provincia = forms.ModelChoiceField(queryset=Provincia.objects.all(), required=True, empty_label="Seleccione una provincia")
    canton = forms.ModelChoiceField(queryset=Canton.objects.none(), required=True, empty_label="Seleccione un cantón")
    distrito = forms.ModelChoiceField(queryset=Distrito.objects.none(), required=True, empty_label="Seleccione un distrito")

    def __init__(self, *args, **kwargs):
        conductores = kwargs.pop('conductores', None)
        vehiculos = kwargs.pop('vehiculos', None)
        super(RutaForm, self).__init__(*args, **kwargs)
        if conductores:
            self.fields['nombre_conductor'].queryset = conductores
        if vehiculos:
            self.fields['id_vehiculo'].queryset = vehiculos


