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
        self.request_user = kwargs.pop('request_user', None)
        super().__init__(*args, **kwargs)

    def clean_role(self):
        role = self.cleaned_data.get('role')
        if self.instance == self.request_user and self.instance.role != role:
            raise ValidationError("No puedes cambiar tu propio rol.")
        return role

    def clean(self):
        cleaned_data = super().clean()

        if self.instance == self.request_user:
            restricted_fields = ['username', 'first_name', 'last_name', 'email']
            for field in restricted_fields:
                if cleaned_data.get(field) != getattr(self.instance, field):
                    self.add_error(field, "No puedes cambiar tus propios datos personales.")
        return cleaned_data
        

class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
        
class CambiarContrasenaForm(forms.Form):
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Nueva Contraseña",
        required=True
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirma Nueva Contraseña",
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password != confirm_password:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")
        return cleaned_data