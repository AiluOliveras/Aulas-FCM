from django.db import models

class Entidades(models.Model):
    """
    Representa el personal de una materia o ente que precise y pueda reservar un aula

    Atributos:
        nombre: String nombre de la entidad
        descripcion: String con una descripcion sobre la actividad de la entidad
        email: String correo electronico para comunicarse con la entidad
        telefono: String telefono para comunicarse con la entidad
    
    """

    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=254)
    email = models.EmailField(max_length=254)
    telefono = models.CharField(max_length=100, null=True, blank=True)