from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Event

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def format_time_popover(self, hora):
        return hora.strftime("%H:%M")
    
    def format_time_evento(self,hora):
        return hora.strftime("%H")

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events, act):
        events_per_day = events.filter(start_time__day=day)
        d = ''
        for event in events_per_day: # Caja del evento en el calendario
            d += f'<li data-toggle="popover" title="<b>{event.entidad.nombre}</b>" data-content="<b>Hora inicio:</b> {self.format_time_popover(event.start_time)}<br/> <b>Hora fin:</b> {self.format_time_popover(event.end_time)}</br> <b>Descripción:</b> {event.description}" data-html="true" style="list-style-type:none;border-radius: 3px;background: #96d4b6;margin-bottom:1px;cursor: pointer;"><b>{self.format_time_evento(event.start_time)}</b> {event.entidad.nombre} </li>'
        
        if day:
            if (act and day==datetime.now().date().day):
                return f"<td style='vertical-align:top;background-color: #E0E0E0;'><span class='date'>{day}</span><ul style='padding: 0px 0px 0px 0px;'> {d} </ul></td>" # Texto del num. de día y eventos
            else:
                return f"<td style='vertical-align:top;'><span class='date'>{day}</span><ul style='padding: 0px 0px 0px 0px;'> {d} </ul></td>" # Texto del num. de día y eventos
        return '<td> </td>'

    # formats a week as a tr 
    def formatweek(self, theweek, events, act):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events, act)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True, aula=None):
        events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)
        if (aula):
            events = events.filter(aula_id=aula).order_by('start_time') #filtro por AULA
        else:
            events = Event.objects.none()
        
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'<tr style="border-color:#E0E0E0;" ><th colspan="7" class="month" style="font-size:120%;">{self.changemonthlang(self.month)} {self.year}</th></tr>\n' #mes en español
        cal += f'<tr style="background-color: #E0E0E0;border-color:#E0E0E0;"><th class="mon">Lun</th><th class="tue">Mar</th><th class="wed">Miér</th><th class="thu">Jue</th><th class="fri">Vier</th><th class="sat">Sab</th><th class="sun">Dom</th></tr>\n' #dia de sem español
        for week in self.monthdays2calendar(self.year, self.month): #une nombre del dia de la semana con num del mes
            #cal += f'{self.formatweek(week, events)}\n'
            if (datetime.now().date().year == self.year) and (datetime.now().date().month == self.month):
                cal += f'{self.formatweek(week, events,True)}\n'
            else:
                cal += f'{self.formatweek(week, events,False)}\n'
        return cal

    def changemonthlang(self,num):
        if num == 1:
            return "Enero"
        elif num == 2:
            return "Febrero"
        elif num == 3:
            return "Marzo"
        elif num == 4:
            return "Abril"
        elif num == 5:
            return "Mayo"
        elif num == 6:
            return "Junio"
        elif num == 7:
            return "Julio"
        elif num == 8:
            return "Agosto"
        elif num == 9:
            return "Septiembre"
        elif num == 10:
            return "Octubre"
        elif num == 11:
            return "Noviembre"
        else: #mes 12
            return "Diciembre"
    