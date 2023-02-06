from django.db import models
from django.forms import ModelForm
from django import forms
from .models import Aulas, Edificios, Entidades
from django import forms
from django.contrib.auth.models import User

class AulasForm(ModelForm):

    class Meta:
        model = Aulas
        fields = ['nombre', 'capacidad', 'conectividad', 'proyector', 'edificio']

class EdificiosForm(ModelForm):

    class Meta:
        model = Edificios
        fields = ['nombre', 'ubicacion']

class EntidadesForm(ModelForm):

    class Meta:
        model = Entidades
        fields = ['nombre', 'descripcion', 'email', 'telefono']

class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['email']
