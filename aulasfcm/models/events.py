from django.db import models

class Event(models.Model): #Reservas
    title = models.CharField(max_length=200)
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
