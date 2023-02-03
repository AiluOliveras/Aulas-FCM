from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from ..models import Entidades

from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django import forms
from ..forms import EntidadesForm


class EntidadesList(ListView):
    model = Entidades

    ordering = ['-nombre']

class EntidadesList(ListView):
    model = Entidades
    paginate_by = 5

    ordering = ['-id']

class EntidadesCreate(SuccessMessageMixin, CreateView):
    form_class = EntidadesForm
    success_message = 'Entidad creada exitosamente!'
    
    def get_success_url(self):
        return reverse('entidades')

class EntidadesDetail(DetailView):
    model = Entidades

class EntidadesUpdate(SuccessMessageMixin, UpdateView):
    model = Entidades
    form_class = EntidadesForm
    success_message = 'Entidad actualizada exitosamente!'

    def get_success_url(self):
        return reverse('entidades')

class EntidadesDelete(SuccessMessageMixin, DeleteView):
    model = Entidades
    form = Entidades
    fields = "__all__"

    def get_success_url(self):
        success_message = 'Entidad eliminada exitosamente!'
        messages.success (self.request, (success_message))
        return reverse('entidades')