from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil

class RegistroForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Requerido.', label='Nombre')
    last_name = forms.CharField(max_length=30, required=True, help_text='Requerido.', label='Apellido')
    email = forms.EmailField(max_length=254, help_text='Requerido. Ingresa un correo válido.', label='Correo Electrónico')
    placa = forms.CharField(max_length=6, required=False, help_text='Opcional. Formato: ABC123', label='Placa del Vehículo (Opcional)')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'placa')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Perfil.objects.create(user=user, placa=self.cleaned_data.get('placa', '').upper())
        return user
