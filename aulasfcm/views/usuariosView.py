from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse
from ..forms import UpdateUserForm
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
from django.views.generic import ListView
from ..models import Edificios

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

class UsuariosList(ListView):
    model = User
    paginate_by = 6

    ordering = ['username']

    def get_queryset(self):
        filtro_edificio= self.request.GET.get("filtro_edificio") #param para saber si es para filtrar users
        username = self.request.GET.get('username')
        if filtro_edificio:
    
            edificio= self.request.GET.get("edificio_id")
            edificio = Edificios.objects.get(id=edificio)

            #retorno users que no son gestores de este edificio
            gestores=[]
            for gest in edificio.gestores.all():
                gestores.append(gest.id) #guardo gestores

            #filtro los que son gestores
            queryset = User.objects.exclude(id__in=gestores)

            if (username):
                queryset = queryset.filter(username__icontains=username)
        else:
            #retorno todos los user
            queryset = User.objects.all()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(UsuariosList, self).get_context_data(**kwargs) # GET de la data default
        #context['usuarios'] = User.objects.all()# Agrego listado de edificios al contexto
        context['filtro_edificio'] = self.request.GET.get('filtro_edificio', 'None')
        edificio= self.request.GET.get("edificio_id")

        context['edificio_obj'] = Edificios.objects.get(id=edificio) # Agrego edificio seleccionado al contexto

        return context