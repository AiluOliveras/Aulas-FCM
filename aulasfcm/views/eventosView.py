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
        """ Calcula el siguiente weekday (por ejemplo, el siguiente lunes o martes de una fecha).

        Args:
            d: Date dia desde el cual se quiere obtener el siguiente weekday
            weekday: Integer dia a obtener

        Returns:
            Fecha del proximo weekday.

        """

        days_ahead = weekday - d.weekday()
        if days_ahead <= 0: # Target day already happened this week
            days_ahead += 7
        return d + datetime.timedelta(days_ahead)

    def form_invalid(self, form):
        """ Crea el alta de un evento con un form personalizado.

        Args:
            aula_id: Integer ID del aula de la cual se quieren conocer sus horarios libres
            fecha_inicio: Date fecha inicio del rango de creacion del evento
            fecha_fin: Date fecha fin del rango de creacion del evento
            hora_inicio: Date (horario) de inicio del evento
            hora_fin: Date (horario) de fin del evento
            aula: FK con la tabla aula, es el aula sobre la cual se realiza la reserva
            dias: Array de dias de la semana elegidos
            descripcion: String descripcion de la reserva
            entidades: FK con la tabla entidades, es la entidad que realiza la reserva

        Returns:
            Redirección hacia el template de creacion con un mensaje de operacion exitosa.

        Raises:
            Redirects con mensajes de error por colision o error por falta de seleccion de almenos un dia de la semana.

        """

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
        """ Retorna un listado de reservas.

        Args:
            aula_id: Integer ID del aula de la cual se quieren conocer sus horarios libres
            entidad_id: Integer ID de la entidad sobre la cual se quieren conocer sus reservas
            fecha_ini: Date fecha inicio del rango en el que se quieren buscar horarios libres
            fecha_fi: Date fecha fin del rango en el que se quieren buscar horarios libres

        Returns:
            Redirección hacia el template de búsqueda con los resultados de la consulta.

        """
        
        aula_id = request.POST.get('aula', None)
        entidad_id = request.POST.get('entidad', None)
        fecha_ini = request.POST.get('fecha_inicio', None)
        fecha_fi = request.POST.get('fecha_fin', None)

        #return HttpResponseRedirect('/eventos/reservas?fecha_inicio='+str(fecha_ini)+'&fecha_fin='+str(fecha_fi)+'&aula='+str(aula_id)+'&entidad='+str(entidad_id))
        return HttpResponseRedirect(f'/eventos/reservas?fecha_inicio={str(fecha_ini)}&fecha_fin={str(fecha_fi)}&aula={str(aula_id)}&entidad={str(entidad_id)}')

class EventoDelete(SuccessMessageMixin, DeleteView):
    model = Event
    fields = "__all__"
    #permission_required = 'delete_event'

    def get(self,aux,pk):
        """ Borra el evento seleccionado (unicamente).

        Args:
            pk: Integer ID del evento a eliminar

        Returns:
            Redirección a la url exitosa junto con un mensaje de resultado de la operacion.
        
        """

        evento= Event.objects.get(id=pk)

        if (evento): #si existe
            if (evento.siguiente_id==None):
                #es el último o era un evento único
                evento.delete()
            else:
                #tiene siguiente
                evento_previo=None
                try:
                    evento_previo=Event.objects.get(siguiente_id=pk)
                except Exception as e:
                    pass
    
                if evento_previo:
                    evento_previo.siguiente_id=evento.siguiente_id
                    evento_previo.save()
                    evento.delete()

                else:
                    evento.delete()

        messages.success(self.request,('Reserva dada de baja exitosamente!'))
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER')) #recargo pag de gestores base

class EventosDelete(SuccessMessageMixin, DeleteView):
    model = Event
    fields = "__all__"

    def get(self,aux,pk):
        """ Borra el evento seleccionado y todos sus relacionados.

        Args:
            pk: Integer ID del evento a eliminar

        Returns:
            Redirección a la url exitosa junto con un mensaje de resultado de la operacion.

        """

        evento= Event.objects.get(id=pk)

        if (evento): #si existe
            if (evento.siguiente_id==None):

                evento_previo=None
                try:
                    evento_previo=Event.objects.get(siguiente_id=pk)
                except Exception as e:
                    pass

                if not evento_previo: #si era un evento único
                    evento.delete()

                else: #es el último de una lista
                    eventos=[]
                    eventos.append(evento) #guardo el evento act (el ultimo)
                    hay_anterior=True

                    while hay_anterior:
                        eventos.append(evento_previo) #guardo el evento ant en la lista
                        try:
                            evento_previo=Event.objects.get(siguiente_id=evento_previo.id)
                        except Exception as e:
                            hay_anterior=False

                    for evento in eventos: #borrado
                        evento.delete()

            else:
                evento_previo= None
                try:
                    evento_previo=Event.objects.get(siguiente_id=pk)
                except Exception as e:
                    pass

                eventos=[]
                eventos.append(evento) #guardo el evento act (el ultimo)
                hay_anterior=True

                #guardo los ants
                while hay_anterior:
                    eventos.append(evento_previo) #guardo el evento ant en la lista
                    try:
                        evento_previo=Event.objects.get(siguiente_id=evento_previo.id)
                    except Exception as e:
                        hay_anterior=False

                #guardo los siguientes
                while (evento.siguiente_id != None):
                    eventos.append(evento)
                    evento=Event.objects.get(id=evento.siguiente_id)
                eventos.append(evento)

                eventos=list(set(eventos))
                for evento in eventos: #borrado
                    evento.delete()

        messages.success(self.request,('Reservas dadas de baja exitosamente!'))
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER')) #recargo pag de gestores base

class HorariosLibresList(ListView):
    model = Event
    #context_object_name = 'event'
    #template_name = 'eventos/reservas.html'
    

    ordering = ['id',]

    def date_front_format(self, adate):
        """ Retorna fechas en un formato acorde a como se quieren mostrar en el frontend.

        Args:
            adate: Date fecha de la cual quiere cambiarse su formato

        Returns:
            Fecha con nuevo formato, en espanol.

        """

        x=["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
        return adate.strftime(x[adate.weekday()]+' '+'%d/%m/%Y, %I:%M %P.')

    def get_context_data(self, **kwargs):
        context = super(HorariosLibresList, self).get_context_data(**kwargs) # GET de la data default del contexto
        #Agrego elementos a la request para motrar en la view
        context['aulas'] = Aulas.objects.all()

        aula= self.request.GET.get("aula")
        if aula:
            context['aula_selected'] = Aulas.objects.get(id=aula)

        fecha_ini= self.request.GET.get("fecha_inicio")
        fecha_fi= self.request.GET.get("fecha_fin")
        if fecha_ini and fecha_fi:
            context['f_inicio'] = fecha_ini
            context['f_fin'] = fecha_fi

        #get eventos en el rango dado y ordenarlos por fecha de inicio
        eventos_list=None
        if (fecha_ini and fecha_fi):
            
            fecha_ini=datetime.datetime.strptime(fecha_ini, "%Y-%m-%d")
            fecha_fi=datetime.datetime.strptime(fecha_fi, "%Y-%m-%d")
            
            eventos_list=Event.objects.filter(aula_id=aula).order_by('start_time')
            eventos_list= eventos_list.filter(start_time__gte=fecha_ini, end_time__lte=fecha_fi)

            evento_ant=None
            data=[]
            libres=[]
            if eventos_list != None:
                #hay eventos
                for evento in eventos_list:
                    if evento_ant != None:
                        #calculo minutos entre el evento anterior y este
                        aux= evento.start_time- evento_ant.end_time
                        minutes = aux.total_seconds() / 60
                        
                        #si el tiempo es mayor a 40min
                        if minutes>40:
                            #lo agrego como horario libre
                            data.append(str(self.date_front_format(evento_ant.end_time)))
                            data.append(str(self.date_front_format(evento.start_time)))

                    else:
                        #es el primero
                        data.append(str(self.date_front_format(fecha_ini)))
                        data.append(str(self.date_front_format(evento.start_time)))
                    
                    evento_ant=evento
                    if (data!=[]):
                        libres.append(data)
                    data=[]
                
                #sumo el tiempo e/ el ultimo evento y el final
                if evento_ant:
                    aux= fecha_fi - evento_ant.end_time
                    minutes = aux.total_seconds() / 60
                        
                    #si el tiempo es mayor a 40min
                    if minutes>40:
                        #lo agrego como horario libre
                        data.append(str(self.date_front_format(evento_ant.end_time)))
                        data.append(str(self.date_front_format(fecha_fi)))
                        libres.append(data)


            else:
                #no hay eventos, todo libre
                data.append(str(self.date_front_format(fecha_ini)))
                data.append(str(self.date_front_format(fecha_fi)))
            
            context['horarios_libres']=libres

        return context

    def post(self, request, *args, **kwargs):
        """ Retorna un listado de horarios libres.

        Args:
            aula_id: Integer ID del aula de la cual se quieren conocer sus horarios libres
            fecha_ini: Date fecha inicio del rango en el que se quieren buscar horarios libres
            fecha_fi: Date fecha fin del rango en el que se quieren buscar horarios libres

        Returns:
            Redirección hacia el template de búsqueda con los resultados de la consulta.

        """

        aula_id = request.POST.get('aula', None)
        fecha_ini = request.POST.get('fecha_inicio', None)
        fecha_fi = request.POST.get('fecha_fin', None)

        #return HttpResponseRedirect('/eventos/horarios_libres?fecha_inicio='+str(fecha_ini)+'&fecha_fin='+str(fecha_fi)+'&aula='+str(aula_id))
        return HttpResponseRedirect(f'/eventos/horarios_libres?fecha_inicio={str(fecha_ini)}&fecha_fin={str(fecha_fi)}&aula={str(aula_id)}')