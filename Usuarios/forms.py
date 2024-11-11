from django import forms
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.core.exceptions import ValidationError

User = get_user_model()



class AgregarPersonalForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirme Contraseña")

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'role']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")
        return cleaned_data

class EditarPersonalForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role']

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user')  # Se recibe el usuario actual desde la vista
        super().__init__(*args, **kwargs)
    
    def clean_role(self):
        role = self.cleaned_data.get('role')
        # Verifica si el usuario actual está editando su propio rol
        if self.instance == self.request_user and self.instance.role != role:
            raise ValidationError("No puedes cambiar tu propio rol.")
        return role
        

class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']