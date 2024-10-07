from django import forms
from .models import Proveedor
 
class ProveedorForm(forms.ModelForm):
    fecha_ingreso = forms.DateField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'date'
    }))
    
    class Meta:
        model = Proveedor
        fields = ['id_proveedor', 'fecha_ingreso', 'nombre_empresa', 'tipo_identificacion', 'identificacion', 'nombre', 'email', 'provincia', 'canton', 'distrito', 'direccion_exacta', 'telefono1', 'telefono2']
        widgets = {
            'id_proveedor': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_ingreso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nombre_empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_identificacion': forms.Select(attrs={'class': 'form-control'}),
            'identificacion': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'provincia': forms.Select(attrs={'class': 'form-control', 'id': 'provincia'}),
            'canton': forms.Select(attrs={'class': 'form-control', 'id': 'canton'}),
            'distrito': forms.Select(attrs={'class': 'form-control', 'id': 'distrito'}),
            'direccion_exacta': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'telefono1': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono2': forms.TextInput(attrs={'class': 'form-control'}),
        }