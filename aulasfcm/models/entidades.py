from django.db import models

class Entidades(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=254)
    email = models.EmailField(max_length=254)
    telefono = models.CharField(max_length=100, null=True, blank=True)