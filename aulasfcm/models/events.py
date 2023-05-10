from django.db import models

class Event(models.Model): #Reservas
    """
    Representa la reserva de un aula.

    Atributos:
        description: String descriptivo sobre el evento
        start_time: DateTime horario de inicio
        end_time: DateTime horario de fin
        aula: FK con la tabla aulas, es el aula sobre la cual se realizo la reserva
        entidad: FK con la tabla entidades, es la entidad que reservo el aula
        siguiente: FK con la tabla event (si misma), indica la reserva siguiente en el caso de las reservas repetidas.

        dia_start: String que indica el dia de inicio del evento en espanol
        dia_end: String que indica el dia de fin del evento en espanol
        
    """

    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    aula = models.ForeignKey('Aulas', on_delete=models.CASCADE)
    entidad = models.ForeignKey('Entidades', on_delete=models.CASCADE)

    siguiente = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    @property
    def dia_start(self):
        x=['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
        return x[self.start_time.weekday()]

    @property
    def dia_end(self):
        x=['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
        return x[self.end_time.weekday()]
