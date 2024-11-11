from django import forms
from .models import Proforma

class ProformaForm(forms.ModelForm):
    class Meta:
        model = Proforma
        fields = '__all__'