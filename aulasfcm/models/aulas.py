from django.db import models

class Aulas(models.Model):
    """
    Representa un aula física dentro de un edificio.

    Atributos:
        nombre: String nombre del aula
        capacidad: Integer cantidad maxima de alumnos
        conectividad: Boolean que indica si tiene o no conexion a internet
        proyector: Boolean que indica si iene o no proyector 
        edificio: FK con la tabla edificios
    
    """

    nombre = models.CharField(max_length=100)
    capacidad = models.IntegerField()
    conectividad = models.BooleanField(default=False)
    proyector = models.BooleanField(default=False)
    
    edificio = models.ForeignKey('Edificios', on_delete=models.CASCADE)