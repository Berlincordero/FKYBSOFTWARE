# forms.py
from django import forms
from .models import OrdenDeCompra

class OrdenDeCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenDeCompra
        fields = [
            'id_usuario', 'id_proveedor', 'id_producto',
            'descripcion', 'cantidad', 'precio_unitario', 'descuento', 'metodo_pago', 'proveedor',
            'lugar_entrega', 'notas', 
        ]