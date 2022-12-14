from django.db import models
from django.forms import ModelForm
from django import forms
from .models import Aulas, Edificios

class AulasForm(ModelForm):

    class Meta:
        model = Aulas
        fields = ['nombre', 'capacidad', 'conectividad', 'proyector', 'edificio']

class EdificiosForm(ModelForm):

    class Meta:
        model = Edificios
        fields = ['nombre', 'ubicacion']
