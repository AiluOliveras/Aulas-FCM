from django.db import models
from django.contrib.auth.models import User

class Edificios(models.Model):
    """
    Representa un edifico de la UNLP.

    Atributos:
        nombre: String nombre del edificio
        ubicacion: String dirección donde se ubica el edificio
        gestores: FK con la tabla usuarios, son quienes administrarán la asignación de aulas y horarios.
    
    """

    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)

    gestores = models.ManyToManyField(User)
