from django.db import models
from django.conf import settings
# Create your models here.
class Torneo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateField()
    cupo_maximo = models.IntegerField()
    imagen = models.ImageField(upload_to='IMG/torneos/', null=True, blank=True)
    hora = models.TimeField(null=True, blank=True)
    premio = models.CharField(max_length=200, null=True, blank=True)

    tipo_juego = models.CharField(
        max_length=50,
        choices=[
            ('Bolirana', 'Bolirana'),
            ('Rana', 'Rana'),
            ('Tejo', 'Tejo'),
            ('Billar', 'Billar')
        ],
        null=True,
        blank=True
    )

    estado_reserva = models.CharField(
        max_length=20,
        choices=[('Abiertas', 'Abiertas'), ('Cerradas', 'Cerradas')],
        default='Abiertas'
    )
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
    nombre_equipo = models.CharField(max_length=100, null=True, blank=True)
    numero_personas = models.IntegerField(null=True, blank=True)
    categoria = models.CharField(max_length=50, null=True, blank=True)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.participante} - {self.torneo}"
        