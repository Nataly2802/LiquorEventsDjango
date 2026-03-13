from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import VentaForm
from .models import Venta, DetalleVenta, Producto

# Create your views here.
@login_required
def crear_venta(request):

    if request.method == "POST":

        form = VentaForm(request.POST)

        if form.is_valid():

            producto = form.cleaned_data["producto"]
            cantidad = form.cleaned_data["cantidad"]

            if producto.stock >= cantidad:

                venta = Venta.objects.create(
                    empleado=request.user
                )

                subtotal = producto.precio * cantidad

                DetalleVenta.objects.create(
                    venta=venta,
                    producto=producto,
                    cantidad=cantidad,
                    precio=producto.precio,
                    subtotal=subtotal
                )

                venta.total = subtotal
                venta.save()

                producto.stock -= cantidad
                producto.save()

                return redirect("/")

    else:

        form = VentaForm()

    return render(request, "inventario/venta.html", {
        "form": form
    })