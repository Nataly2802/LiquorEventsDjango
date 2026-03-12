from django.db import models

# Create your models here.
class Torneo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateField()
    cupos = models.IntegerField()
    
    def __str__(self):
        return self.nombre
        