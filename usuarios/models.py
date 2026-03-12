from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Usuario(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('empleado', 'Empleado'),
        ('participante', 'Participante'),
    )
    rol = models.CharField(max_length=20, choices=ROLES)
    
    def __str__(self):
        return self.username
        
