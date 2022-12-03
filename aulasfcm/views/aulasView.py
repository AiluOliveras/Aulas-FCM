from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from ..models import Aulas

from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django import forms


class AulasList(ListView):
    model = Aulas
    paginate_by = 5

    ordering = ['-id']

class AulasCreate(SuccessMessageMixin, CreateView):
    model = Aulas
    form = Aulas
    fields = "__all__"
    success_message = 'Aula creada exitosamente!'
    
    def get_success_url(self):
        return reverse('aulas')

class AulasDetail(DetailView):
    model = Aulas

class AulasUpdate(SuccessMessageMixin, UpdateView):
    model = Aulas
    form = Aulas
    fields = "__all__"
    success_message = 'Aula actualizada exitosamente!'

    def get_success_url(self):
        return reverse('aulas')

class AulasDelete(SuccessMessageMixin, DeleteView):
    model = Aulas
    form = Aulas
    fields = "__all__"

    def get_success_url(self):
        success_message = 'Aula eliminada exitosamente!'
        messages.success (self.request, (success_message))
        return reverse('aulas')