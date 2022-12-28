from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from ..models import Edificios

from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django import forms
from ..forms import EdificiosForm


class EdificiosList(ListView):
    model = Edificios

    ordering = ['-nombre']

class EdificiosList(ListView):
    model = Edificios
    paginate_by = 5

    ordering = ['-id']

class EdificiosCreate(SuccessMessageMixin, CreateView):
    form_class = EdificiosForm
    success_message = 'Edificio creado exitosamente!'
    
    def get_success_url(self):
        return reverse('edificios')

class EdificiosDetail(DetailView):
    model = Edificios

class EdificiosUpdate(SuccessMessageMixin, UpdateView):
    model = Edificios
    form_class = EdificiosForm
    success_message = 'Edificio actualizado exitosamente!'

    def get_success_url(self):
        return reverse('edificios')

class EdificiosDelete(SuccessMessageMixin, DeleteView):
    model = Edificios
    form = Edificios
    fields = "__all__"

    def get_success_url(self):
        success_message = 'Edificio eliminado exitosamente!'
        messages.success (self.request, (success_message))
        return reverse('edificios')