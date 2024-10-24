from django import forms
from .models import OrdenDeCompra
from Inventario.models import Producto
from Proveedores.models import Proveedor        

class OrdenDeCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenDeCompra
        fields = [
            'id_orden',
            'id_usuario',
            'id_proveedor',
            'id_producto',
            'descripcion',
            'cantidad',
            'precio_unitario',
            'proveedor',
            'lugar_entrega',
            'notas',
            'metodo_pago',
            'IVI'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 2}),
            'lugar_entrega': forms.Textarea(attrs={'rows': 2}),
            'notas': forms.Textarea(attrs={'rows': 2}),
            'IVI': forms.NumberInput(attrs={'step': 0.01}),
            'precio_unitario': forms.NumberInput(attrs={'step': 0.01}),
            'cantidad': forms.NumberInput(attrs={'step': 1}),
        }
