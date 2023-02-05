from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from ..models import Entidades

from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django import forms
from ..forms import EntidadesForm
from django.contrib.auth.mixins import PermissionRequiredMixin

class EntidadesList(ListView):
    model = Entidades
    paginate_by = 5

    ordering = ['-id']

    def get_queryset(self):
        nombre = self.request.GET.get('nombre')
        if nombre:
            return Entidades.objects.filter(nombre__icontains=nombre)
        else:
            return Entidades.objects.all()

class EntidadesCreate(SuccessMessageMixin, CreateView):
    form_class = EntidadesForm
    success_message = 'Entidad creada exitosamente!'
    
    def get_success_url(self):
        return reverse('entidades')

class EntidadesDetail(DetailView):
    model = Entidades

class EntidadesUpdate(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Entidades
    form_class = EntidadesForm
    success_message = 'Entidad actualizada exitosamente!'
    permission_required = 'change_entidades'

    def get_success_url(self):
        return reverse('entidades')

class EntidadesDelete(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Entidades
    form = Entidades
    fields = "__all__"
    permission_required = 'delete_entidades'

    def get_success_url(self):
        success_message = 'Entidad eliminada exitosamente!'
        messages.success (self.request, (success_message))
        return reverse('entidades')