from django.db import models

class Aulas(models.Model):
    nombre = models.CharField(max_length=100)
    capacidad = models.IntegerField()
    conectividad = models.BooleanField(default=False)
    proyector = models.BooleanField(default=False)
    
    edificio = models.ForeignKey('Edificios', on_delete=models.CASCADE)