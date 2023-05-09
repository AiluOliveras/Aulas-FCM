from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.utils.safestring import mark_safe

from ..models import *
from ..utils import Calendar
from datetime import timedelta
import calendar
from datetime import date

class CalendarView(generic.ListView):
    model = Event
    template_name = 'calendario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        #d = get_date(self.request.GET.get('day', None))
        
        # Mes anterior y siguiente
        d = get_date(self.request.GET.get('month', None))
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Saco params del header p/ filtros en calendario
        aula= self.request.GET.get("aula") #VALIDAR SI MANDA NONE

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True, aula=aula) # Cabecera + formato texto de eventos
        context['calendar'] = mark_safe(html_cal)

        #Agrego elementos a la request para motrar en la view
        edificio= self.request.GET.get("edificio",None) #VALIDAR SI MANDA NONE
        if (edificio):
            context['aulas'] = Aulas.objects.filter(edificio_id=edificio) #retorno aulas de ese edif
        else:
            context['aulas'] = Aulas.objects.all()[:6] #retorno primeras 6 aulas
        
        if (aula):
            context['aula']= Aulas.objects.get(id=aula) #retorno aula elegida
        
        context['edificios'] = Edificios.objects.all() #retorno edificios

        if (edificio):
            context['edificio']= Edificios.objects.get(id=edificio) #retorno edificio elegido

        #Mes anterior y siguiente
        d = get_date(self.request.GET.get('month', None))
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)

        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    #month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    month = f'month={str(prev_month.year)}-{str(prev_month.month)}'
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    #month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    month = f'month={str(next_month.year)}-{str(next_month.month)}'
    return month