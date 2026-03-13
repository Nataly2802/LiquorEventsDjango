from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import VentaForm
from .models import Venta, DetalleVenta, Producto
from django.utils import timezone
from torneos.models import Torneo
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.db.models import Count
import json
from torneos.models import Torneo
# Create your views here.
def solo_empleados(view_func):
    
    def wrapper(request, *args, **kwargs):

        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        if hasattr(request.user, "rol") and request.user.rol in ["administrador", "empleado"]:
            return view_func(request, *args, **kwargs)

        return HttpResponse("No tienes permiso para acceder a ventas")

    return wrapper

@login_required
@solo_empleados
def crear_venta(request):

    productos = Producto.objects.all()
    torneos = Torneo.objects.all()

    if request.method == "POST":

        torneo_id = request.POST.get("torneo")

        torneo = None

        if torneo_id:
            torneo = Torneo.objects.get(id=torneo_id)

        venta = Venta.objects.create(
            empleado=request.user,
            torneo=torneo
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
        "productos": productos,
        "torneos": torneos
    })
    
@login_required
@solo_empleados
def dashboard(request):
    
    total_ventas = Venta.objects.aggregate(
        total=Sum('total')
    )['total'] or 0

    cantidad_ventas = Venta.objects.count()

    productos = Producto.objects.count()

    torneos = Torneo.objects.count()
    
    ventas_por_dia = (
    Venta.objects
    .annotate(dia=TruncDate('fecha'))
    .values('dia')
    .annotate(total=Sum('total'))
    .order_by('dia')
)

    context = {
    'total_ventas': total_ventas,
    'cantidad_ventas': cantidad_ventas,
    'productos': productos,
    'torneos': torneos,
    'ventas_por_dia': json.dumps(list(ventas_por_dia), default=str)
}

    return render(request, 'inventario/dashboard.html', context)


@login_required
def ticket_pdf(request, venta_id):

    venta = Venta.objects.get(id=venta_id)

    detalles = DetalleVenta.objects.filter(
        venta=venta
    )

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="ticket_{venta.id}.pdf"'

    p = canvas.Canvas(response)

    y = 800

    p.drawString(100, y, "LiquorEvents")
    y -= 30

    p.drawString(100, y, f"Venta #{venta.id}")
    y -= 30

    for d in detalles:

        texto = f"{d.producto.nombre} x{d.cantidad} - ${d.subtotal}"

        p.drawString(100, y, texto)

        y -= 20

    y -= 20

    p.drawString(100, y, f"TOTAL: ${venta.total}")

    p.showPage()
    p.save()

    return response