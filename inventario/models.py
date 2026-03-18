from django.db import models
from django.conf import settings
from torneos.models import Torneo
# Create your models here.

class Producto(models.Model):

    nombre = models.CharField(max_length=200)
    marca = models.CharField(max_length=200)

    precio = models.DecimalField(max_digits=10, decimal_places=2)

    stock = models.IntegerField()

    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre
    
from torneos.models import Torneo

class Venta(models.Model):
    
    empleado = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    torneo = models.ForeignKey(
        Torneo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    total = models.DecimalField(max_digits=10, decimal_places=2)

    pago = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    cambio = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venta #{self.id} - {self.fecha}"
    
class DetalleVenta(models.Model):
    
    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE
    )

    cantidad = models.IntegerField()

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.producto} x {self.cantidad}"