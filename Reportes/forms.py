from django import forms
from .models import PagoFactura

class PagoFacturaForm(forms.ModelForm):
    class Meta:
        model = PagoFactura
        fields = ['numero_factura', 'monto_pago', 'fecha_pago', 'metodo_pago']
        widgets = {
            'fecha_pago': forms.DateInput(attrs={'type': 'date'}),
        }