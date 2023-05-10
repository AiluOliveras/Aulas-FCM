from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView

from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django import forms
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from ..models import Edificios

class GestoresList(ListView):
    model = User
    paginate_by = 6

    ordering = ['username']

    def get_queryset(self):
        edificio= self.request.GET.get('edificio')
        if edificio:
            edificio = Edificios.objects.get(id=edificio)
            queryset = edificio.gestores.all() # Tomo los gestores de determinado edificio

            return queryset

    def get_context_data(self, **kwargs):
        context = super(GestoresList, self).get_context_data(**kwargs) # GET de la data default del contexto
        edificio= self.request.GET.get('edificio')

        context['edificio_obj'] = Edificios.objects.get(id=edificio) # Agrego edificio seleccionado al contexto

        return context