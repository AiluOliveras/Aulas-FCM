from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Event

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events):
        events_per_day = events.filter(start_time__day=day)
        d = ''
        for event in events_per_day:
            d += f'<li style="list-style-type:none;border-radius: 3px;background: #96d4b6;"> {event.title} </li>'  # Texto del evento en el calendario - color

        if day != 0:
            return f"<td style='vertical-align:top;'><span class='date'>{day}</span><ul style='padding: 0px 0px 0px 0px;'> {d} </ul></td>" # Texto del num. de día y eventos
        return '<td> </td>'

    # formats a week as a tr 
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True, aula=None):
        events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)
        if (aula):
            events = events.filter(aula_id=aula) #filtro por AULA
        else:
            events = Event.objects.none()
        #print(self.formatmonthname(self.year, self.month, withyear=withyear))
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        #cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n' #mes en ingles
        cal += f'<tr><th colspan="7" class="month">{self.changemonthlang(self.month)} {self.year}</th></tr>\n' #mes en español
        #cal += f'{self.formatweekheader()}\n' #dia de sem en ingles
        cal += f'<tr><th class="mon">Lun</th><th class="tue">Mar</th><th class="wed">Mier</th><th class="thu">Jue</th><th class="fri">Vier</th><th class="sat">Sab</th><th class="sun">Dom</th></tr>\n' #dia de sem español
        for week in self.monthdays2calendar(self.year, self.month): #une nombre del dia de la semana con num del mes
            cal += f'{self.formatweek(week, events)}\n'
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
    