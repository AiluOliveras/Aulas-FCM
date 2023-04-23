from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from ..models import Event, Aulas, Edificios, Entidades

from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django import forms
from ..forms import EventForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect, HttpResponse
import datetime

class EventCreate(CreateView):
    form_class = EventForm
    success_message = 'Evento creado exitosamente!'
    permission_required = 'add_event'

    def get_context_data(self, **kwargs):
        context = super(EventCreate, self).get_context_data(**kwargs) # GET de la data default del contexto
        if (self.request.user.is_superuser):
            context['edificios'] = Edificios.objects.all().order_by('id')
        else:
            context['edificios'] = Edificios.objects.filter(gestores__id=(self.request.user.id)).order_by('id')
        context['aulas'] = Aulas.objects.filter(edificio_id__in=context['edificios']).order_by('edificio_id','nombre') # Agrego edificio seleccionado al contexto
        context['entidades'] = Entidades.objects.all().order_by('nombre') 

        return context

    def get_success_url(self):
        return reverse('calendario')

    def form_valid(self, form):
        # do something with self.object
        # remember the import: from django.http import HttpResponseRedirect
        print('holauwu')
        return HttpResponseRedirect(self.get_success_url())

    def next_weekday(self, d, weekday):
        days_ahead = weekday - d.weekday()
        if days_ahead <= 0: # Target day already happened this week
            days_ahead += 7
        return d + datetime.timedelta(days_ahead)

    def form_invalid(self, form):

        # tomo data del form

        hora_inicio=form.data['hora_inicio']
        hora_fin=form.data['hora_fin']
        fecha_inicio=form.data['fecha_inicio']
        fecha_fin=form.data['fecha_fin']
        aula=form.data['aula']

        ##print('fecha inicio: '+fecha_inicio+' | hora fin: '+hora_fin+' | aula: '+aula)
        # transformo fechas str en date
        fecha_inicio=datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_fin=datetime.datetime.strptime(fecha_fin, "%Y-%m-%d")
        hora_inicio=datetime.datetime.strptime(hora_inicio,"%H:%M")
        hora_fin=datetime.datetime.strptime(hora_fin,"%H:%M")

        # opero con los checkbox de dias
        dias=["lunes","martes","miercoles","jueves","viernes","sabado","domingo"]
        dias_elegidos=[] #0=lunes, 1=martes ...
        for x,d in enumerate(dias):
            try:
                form.data[str(d)]
                dias_elegidos.append(x)
            except Exception as e:
                pass #no está elegido ese día

        ##print(dias_elegidos)
        # si no eligió dias, retorno error
        if (not dias_elegidos):
            messages.error(self.request,'Debe seleccionar almenos una opción en el apartado "Frecuencia".')
            return HttpResponseRedirect('/eventos/crear')

        ####VALIDA SI ES ALTA ÚNICA O REPETITIVA
        repetir=False
        try:
            repetir= form.data['repetir']
            #print('se repite')
        except Exception as e:
            repetir=False
            #print('no se repite')
        

        ###checkear colisiones de eventos (OVERLAP)###
        eventos= Event.objects.filter(aula_id=aula) # filtrar eventos en esta aula
        #filtro por fechas
        for dia in dias_elegidos:
            fecha_base=self.next_weekday(fecha_inicio,dia) #ej:primer lunes del rango
            #fecha base + hora inicio 
            fecha_base=fecha_base.replace(hour=(hora_inicio.hour), minute=(hora_inicio.minute))
            fecha_base_fin=fecha_base.replace(hour=(hora_fin.hour), minute=(hora_fin.minute))
            ##print('fecha del próximo '+str(dia)+': '+str(fecha_base)+' a '+str(fecha_base_fin))
            
            while fecha_base <= fecha_fin:  #mientras no llegue a la fecha de fin
                ##print('fecha act <= fecha fin')
                
                colisiones_l=eventos.filter(
                end_time__gte=fecha_base,
                start_time__lte=fecha_base_fin
                )

                # checkeo colision de horario
                if (colisiones_l.count() >0):
                    messages.error(self.request,'No se pudo dar de alta el evento ya que colisiona con otro: '+(colisiones_l.first().entidad.nombre))
                    return HttpResponseRedirect('/eventos/crear')

                fecha_base += datetime.timedelta(weeks=1) #siguiente lunes
                fecha_base_fin += datetime.timedelta(weeks=1)
                #print(str(fecha_base))
        
        # si llego aca, no hay overlap. procedo al alta
        ##print("------------No hay colisiones, procede al alta.---------------")

        ###ALTA###
        #dias_elegidos= checkbox
        actual=fecha_inicio
        evento_ant=None
        while actual <= fecha_fin:
            ##print("Alta- una vuelta mas: "+str(actual.weekday())+"  -  " + str(actual))
            if ((actual.weekday()) in (dias_elegidos)):  #si el día actual esta en los dias elegidos
                ##print('^ Este día fue elegido.')
                evento_nuevo= Event.objects.create(description=form.data['description'],entidad_id=form.data['entidades'],aula_id=aula,start_time=(actual.replace(hour=(hora_inicio.hour), minute=(hora_inicio.minute))),end_time=(actual.replace(hour=(hora_fin.hour), minute=(hora_fin.minute))))  #creo el evento (fecha: actual. horario: del form.)
                if (evento_ant):
                    evento_ant.siguiente_id= evento_nuevo.id
                    evento_ant.save()
                evento_ant = evento_nuevo  #actualizo referencias
                ##print(str(evento_nuevo))
            #avanzamos al dia siguiente
            actual += datetime.timedelta(days=1)
        
        #redirect exitoso
        messages.success(self.request,('Evento dado de alta exitosamente!'))
        return HttpResponseRedirect('/eventos/crear')

class EventosListResponse(ListView):
    model = Event
    paginate_by = 10

    ordering = ['-id']
    template_name = 'eventos/reservas.html'


class EventosList(ListView):
    model = Event
    paginate_by = 10
    #context_object_name = 'event'
    #template_name = 'eventos/reservas.html'
    

    ordering = ['id',]

    def get_context_data(self, **kwargs):
        context = super(EventosList, self).get_context_data(**kwargs) # GET de la data default del contexto
        #Agrego elementos a la request para motrar en la view
        context['aulas'] = Aulas.objects.all()
        context['entidades'] = Entidades.objects.all()

        aula= self.request.GET.get("aula")
        if aula:
            #print(aula)
            context['aula_selected'] = Aulas.objects.get(id=aula)

        ent= self.request.GET.get("entidad")
        if ent:
            context['entidad_selected'] = Entidades.objects.get(id=ent)

        fecha_ini= self.request.GET.get("fecha_inicio")
        fecha_fi= self.request.GET.get("fecha_fin")
        if fecha_ini and fecha_fi:
            context['f_inicio'] = fecha_ini
            context['f_fin'] = fecha_fi

        #Agrego edifs que administra para validar en la view
        context['permitidos']= ((Edificios.objects.filter(gestores__id=(self.request.user.id)))).values_list('id', flat=True)
        
        return context
    
    def get_queryset(self):
        query= None
        aula= self.request.GET.get('aula')
        if aula:
            query= Event.objects.filter(aula_id=aula).order_by('-id')
        else:
            query= Event.objects.all().order_by('-id')

        ent = self.request.GET.get('entidad')
        if ent:
            query= query.filter(entidad_id=ent)

        fecha_inicio= self.request.GET.get('fecha_inicio')
        fecha_fin= self.request.GET.get('fecha_fin')

        if (fecha_inicio and fecha_fin):
            #print('busq x fechas')
            fecha_inicio=datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin=datetime.datetime.strptime(fecha_fin, "%Y-%m-%d")
            
            query= query.filter(start_time__gte=fecha_inicio, end_time__lte=fecha_fin)
        return query

    def post(self, request, *args, **kwargs):
        aula_id = request.POST.get('aula', None)
        entidad_id = request.POST.get('entidad', None)
        fecha_ini = request.POST.get('fecha_inicio', None)
        fecha_fi = request.POST.get('fecha_fin', None)

        return HttpResponseRedirect('/eventos/reservas?fecha_inicio='+str(fecha_ini)+'&fecha_fin='+str(fecha_fi)+'&aula='+str(aula_id)+'&entidad='+str(entidad_id))