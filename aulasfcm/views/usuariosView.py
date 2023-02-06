from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse
from ..forms import UpdateUserForm
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView

class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm


class CustomPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    extra_context = {'done': 'done'}

class UsuariosUpdate(UpdateView):
    model = User
    form_class = UpdateUserForm
    success_message = 'Email actualizado exitosamente!'

    def get_success_url(self):
        return reverse('cambiar-email/exitoso')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(UsuariosUpdate, self).get_context_data(**kwargs) # GET de la data default
        context['mail'] = (User.objects.get(id=self.request.user.id)).email # Agrego listado de edificios al contexto

        return context

class CustomUsuariosUpdate(UpdateView):
    model = User
    form_class = UpdateUserForm
    success_message = 'Email actualizado exitosamente!'
    extra_context = {'done': 'done'}

    def get_success_url(self):
        return reverse('cambiar-email/exitoso')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(CustomUsuariosUpdate, self).get_context_data(**kwargs) # GET de la data default
        context['mail'] = (User.objects.get(id=self.request.user.id)).email # Agrego listado de edificios al contexto

        return context