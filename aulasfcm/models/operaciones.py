from django.db import models
from django.contrib.auth.models import User

class Operaciones(models.Model):
    operacion = models.CharField(max_length=10)
    endpoint = models.CharField(max_length=150)
    fecha = models.DateTimeField()
    
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)