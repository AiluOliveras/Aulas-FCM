from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from ..models import Edificios

from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django import forms
from ..forms import EdificiosForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages

class EdificiosList(ListView):
    model = Edificios
    paginate_by = 5

    ordering = ['-id']

class EdificiosCreate(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = EdificiosForm
    success_message = 'Edificio creado exitosamente!'
    permission_required = 'add_edificios'
    
    def get_success_url(self):
        return reverse('edificios')

class EdificiosDetail(DetailView):
    model = Edificios

class EdificiosUpdate(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Edificios
    form_class = EdificiosForm
    success_message = 'Edificio actualizado exitosamente!'
    permission_required = 'change_edificios'

    def get_success_url(self):
        return reverse('edificios')

class EdificiosDelete(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Edificios
    form = Edificios
    fields = "__all__"
    permission_required = 'delete_edificios'

    def get_success_url(self):
        success_message = 'Edificio eliminado exitosamente!'
        messages.success (self.request, (success_message))
        return reverse('edificios')

    
def destroy_gestor_edificio(request, *args, **kwargs):
    from django.contrib.auth.models import User
    gestor= request.GET.get("gestor")
    edificio= request.GET.get("edificio")

    if edificio and gestor:

        #se elimina permiso del gestor sobre el edificio dado
        edificio_up = Edificios.objects.get(id=edificio)
        gestor_up = User.objects.get(id=gestor)
        edificio_up.gestores.remove(gestor_up)

        messages.success(request,('Gestor dado de baja exitosamente!'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) #recargo pag de gestores base

    return HttpResponse("Hubo un error, por favor regrese a la página anterior.")
