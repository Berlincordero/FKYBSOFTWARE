# forms.py

from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=200)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class MiFormulario(forms.Form):
    # Define los campos que necesitas
    campo1 = forms.CharField(max_length=100)
    campo2 = forms.EmailField()
    # Agrega más campos según sea necesario
