from django.contrib import admin
from .models import Producto, Venta, DetalleVenta

# Register your models here.

class VentaAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "empleado",
        "torneo",
        "total",
        "fecha"
    )


admin.site.register(Producto)
admin.site.register(DetalleVenta)
admin.site.register(Venta, VentaAdmin)