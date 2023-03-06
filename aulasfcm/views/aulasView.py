from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from ..models import Aulas, Edificios

from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django import forms
from ..forms import AulasForm
from django.contrib.auth.mixins import PermissionRequiredMixin

class AulasList(ListView):
    model = Aulas
    paginate_by = 5

    ordering = ['nombre']

class AulasCreate(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = AulasForm
    success_message = 'Aula creada exitosamente!'
    permission_required = 'add_aulas'
    
    def get_success_url(self):
        return reverse('aulas')

    def get_context_data(self, **kwargs):
        context = super(AulasCreate, self).get_context_data(**kwargs) # GET de la data default del contexto
        context['edificios'] = Edificios.objects.all() # Agrego listado de edificios al contexto
        return context

class AulasDetail(DetailView):
    model = Aulas

class AulasUpdate(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Aulas
    form_class = AulasForm
    success_message = 'Aula actualizada exitosamente!'
    permission_required = 'change_aulas'

    def get_success_url(self):
        return reverse('aulas')

    def get_context_data(self, **kwargs):
        context = super(AulasUpdate, self).get_context_data(**kwargs) # GET de la data default
        context['edificios'] = Edificios.objects.all() # Agrego listado de edificios al contexto
        return context

class AulasDelete(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Aulas
    form = Aulas
    fields = "__all__"
    permission_required = 'delete_aulas'

    def get_success_url(self):
        success_message = 'Aula eliminada exitosamente!'
        messages.success (self.request, (success_message))
        return reverse('aulas')