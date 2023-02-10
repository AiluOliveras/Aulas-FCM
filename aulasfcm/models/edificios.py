from django.db import models
from django.contrib.auth.models import User

class Edificios(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)

    gestores = models.ManyToManyField(User)
