# forms.py
from django import forms
from .models import OrdenDeCompra
from Proveedores.models import Proveedor

class OrdenDeCompraForm(forms.ModelForm):
    proveedor = forms.ModelChoiceField(
        queryset=Proveedor.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Proveedor"
    )
    class Meta:
        model = OrdenDeCompra
        fields = [
            'producto', 'descripcion', 'cantidad', 'precio_unitario',
            'proveedor', 'notas', 'metodo_pago', 'total'
        ]
