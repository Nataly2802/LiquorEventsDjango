from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import VentaForm
from .models import Venta, DetalleVenta, Producto

# Create your views here.
@login_required
def crear_venta(request):

    productos = Producto.objects.all()

    if request.method == "POST":

        venta = Venta.objects.create(
            empleado=request.user
        )

        total = 0

        for producto in productos:

            cantidad = request.POST.get(f"cantidad_{producto.id}")

            if cantidad:

                cantidad = int(cantidad)

                if cantidad > 0 and producto.stock >= cantidad:

                    subtotal = producto.precio * cantidad

                    DetalleVenta.objects.create(
                        venta=venta,
                        producto=producto,
                        cantidad=cantidad,
                        precio=producto.precio,
                        subtotal=subtotal
                    )

                    producto.stock -= cantidad
                    producto.save()

                    total += subtotal

        venta.total = total
        venta.save()

        return redirect("/venta/")

    return render(request, "inventario/venta.html", {
        "productos": productos
    })