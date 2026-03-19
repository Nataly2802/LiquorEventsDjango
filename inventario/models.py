from django.db import models
from django.conf import settings
from torneos.models import Torneo
# Create your models here.

class Producto(models.Model):
    
    codigo = models.CharField(max_length=50, unique=True,)

    nombre = models.CharField(max_length=200)
    marca = models.CharField(max_length=200)

    categoria = models.CharField(max_length=100, default='General')

    precio = models.DecimalField(max_digits=10, decimal_places=2)

    stock = models.IntegerField()

    estado = models.CharField(
        max_length=20,
        choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')],
        default='Activo'
    )

    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre
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
    
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto} x {self.cantidad}"
    
class MovimientoInventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo = models.CharField(
        max_length=10,
        choices=[('Entrada', 'Entrada'), ('Salida', 'Salida')]
    )
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    motivo = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} ({self.cantidad})"
    
class Compra(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    proveedor = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Compra - {self.producto.nombre}"