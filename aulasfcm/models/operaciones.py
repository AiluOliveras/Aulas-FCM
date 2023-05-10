from django.db import models
from django.contrib.auth.models import User

class Operaciones(models.Model):
    """
    Es una tabla de logs personalizados.

    Atributos:
        operacion: String que indica el tipo de operacion realizada, GET/POST/PUT/DELETE
        endpoint: String url del sistema sobre el cual realizo la operacion
        fecha: DateTime que indica la fecha de cuando se realizo la operacion
        usuario: FK con la tabla usuarios, es el autor de la operacion.
    
    """

    operacion = models.CharField(max_length=10)
    endpoint = models.CharField(max_length=150)
    fecha = models.DateTimeField()
    
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)