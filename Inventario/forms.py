# inventario/forms.py
from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto  # Asegúrate de que el modelo esté importado correctamente
        fields = '__all__'  