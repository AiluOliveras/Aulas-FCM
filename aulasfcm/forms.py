from django.db import models
from django.forms import ModelForm, DateInput
from django import forms
from .models import Aulas, Edificios, Entidades, Event
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

class EventForm(ModelForm):
  class Meta:
    model = Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)

