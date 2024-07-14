from django import forms


# Usuarios/forms.py

from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=200)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
