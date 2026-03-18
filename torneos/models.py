from django.db import models
from django.conf import settings
# Create your models here.
class Torneo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateField()
    cupo_maximo = models.IntegerField()
    imagen = models.ImageField(upload_to='IMG/torneos/', null=True, blank=True)
    
    def __str__(self):
        return self.nombre
    
class Inscripcion(models.Model):
    
    participante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    torneo = models.ForeignKey(
        Torneo,
        on_delete=models.CASCADE
    )

    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.participante} - {self.torneo}"
        