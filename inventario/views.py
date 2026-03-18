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
import openpyxl
from django.contrib import messages
from django.db import transaction
from django.utils.dateparse import parse_date
from reportlab.lib.pagesizes import letter
from openpyxl.styles import Font
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os
from django.conf import settings
# Create your views here.
def solo_empleados(view_func):
    
    def wrapper(request, *args, **kwargs):

        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        if hasattr(request.user, "rol") and request.user.rol in ["admin", "empleado"]:
            return view_func(request, *args, **kwargs)

        return HttpResponse("No tienes permiso para acceder a ventas")

    return wrapper

@login_required
@solo_empleados
@transaction.atomic
def crear_venta(request):

    productos = Producto.objects.all()
    torneos = Torneo.objects.all()

    if request.method == "POST":

        torneo_id = request.POST.get("torneo")
        pago = float(request.POST.get("pago") or 0)

        torneo = None
        if torneo_id:
            torneo = Torneo.objects.get(id=torneo_id)

        total = 0
        detalles = []

        for producto in productos:
            cantidad = int(request.POST.get(f"cantidad_{producto.id}") or 0)

            if cantidad > 0:

                if cantidad > producto.stock:
                    messages.error(request, f"Stock insuficiente para {producto.nombre}")
                    return redirect("/venta/")

                subtotal = float(producto.precio) * cantidad
                total += subtotal

                detalles.append({
                    "producto": producto,
                    "cantidad": cantidad,
                    "precio": producto.precio,
                    "subtotal": subtotal
                })

        if total == 0:
            messages.error(request, "Debe seleccionar al menos un producto")
            return redirect(f"/ticket/{venta.id}/")

        if pago < total:
            messages.error(request, "El pago es insuficiente")
            return redirect("/venta/")

        cambio = pago - total

        venta = Venta.objects.create(
            empleado=request.user,
            torneo=torneo,
            total=total,
            pago=pago,
            cambio=cambio
        )

        for d in detalles:
            DetalleVenta.objects.create(
                venta=venta,
                producto=d["producto"],
                cantidad=d["cantidad"],
                precio=d["precio"],
                subtotal=d["subtotal"]
            )

            producto = d["producto"]
            producto.stock -= d["cantidad"]
            producto.save()

        messages.success(request, f"Venta registrada correctamente. Cambio: ${cambio}")

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
    ventas = (
    Venta.objects
    .values("torneo__nombre")
    .annotate(total=Sum("total"))
)

    ventas_por_torneo = []

    for torneo in Torneo.objects.all():
        total = Venta.objects.filter(torneo=torneo).aggregate(total=Sum("total"))["total"] or 0
        ventas_por_torneo.append({
            "torneo": torneo.nombre,
            "total": int(total) 
        })

    total_normal = Venta.objects.filter(torneo__isnull=True).aggregate(total=Sum("total"))["total"] or 0
    ventas_por_torneo.append({
        "torneo": "Venta normal",
        "total": int(total_normal)
    })

    productos_mas_vendidos = (
    DetalleVenta.objects
    .values("producto__nombre")
    .annotate(total_vendido=Sum("cantidad"))
    .order_by("-total_vendido")[:5]
)
    inventario_bajo = Producto.objects.filter(stock__lte=5)
    
    context = {
    'total_ventas': total_ventas,
    'cantidad_ventas': cantidad_ventas,
    'productos': productos,
    'torneos': torneos,
    'ventas_por_dia': json.dumps(list(ventas_por_dia), default=str),
    'ventas_por_torneo': json.dumps(ventas_por_torneo),
    'productos_mas_vendidos': productos_mas_vendidos,
    'inventario_bajo': inventario_bajo
}

    return render(request, 'inventario/dashboard.html', context)



@login_required
def ticket_pdf(request, venta_id):

    venta = Venta.objects.get(id=venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename=recibo_{venta.id}.pdf'

    doc = SimpleDocTemplate(response, pagesize=letter)

    styles = getSampleStyleSheet()
    elements = []

    logo_path = os.path.join(settings.BASE_DIR, 'static/IMG/logo.jpg')
    if os.path.exists(logo_path):
        elements.append(Image(logo_path, width=80, height=80))

    elements.append(Paragraph("<b>LiquorEvents</b>", styles['Title']))
    elements.append(Paragraph("NIT: 123456789", styles['Normal']))
    elements.append(Paragraph("Bogotá, Colombia", styles['Normal']))
    elements.append(Spacer(1, 10))

    fecha_formateada = venta.fecha.strftime("%d/%m/%Y %H:%M")

    elements.append(Paragraph(f"<b>Factura N°:</b> {venta.id}", styles['Normal']))
    elements.append(Paragraph(f"<b>Fecha:</b> {fecha_formateada}", styles['Normal']))
    elements.append(Paragraph(f"<b>Empleado:</b> {venta.empleado.username}", styles['Normal']))

    if venta.torneo:
        elements.append(Paragraph(f"<b>Torneo:</b> {venta.torneo.nombre}", styles['Normal']))
    else:
        elements.append(Paragraph("<b>Tipo:</b> Venta normal", styles['Normal']))

    elements.append(Spacer(1, 10))

    data = [["Producto", "Cant", "Precio", "Subtotal"]]

    for d in detalles:
        data.append([
            d.producto.nombre,
            d.cantidad,
            f"${int(d.precio)}",
            f"${int(d.subtotal)}"
        ])

    table = Table(data)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.black),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),

        ('GRID', (0,0), (-1,-1), 1, colors.grey),

        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 15))

    elements.append(Paragraph(f"<b>Total:</b> ${int(venta.total)}", styles['Normal']))
    elements.append(Paragraph(f"<b>Pago:</b> ${int(venta.pago)}", styles['Normal']))
    elements.append(Paragraph(f"<b>Cambio:</b> ${int(venta.cambio)}", styles['Normal']))

    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Gracias por su compra", styles['Italic']))

    doc.build(elements)

    return response

@login_required
@solo_empleados
def lista_ventas(request):
    
    ventas = Venta.objects.all().order_by('-fecha')

    fecha = request.GET.get('fecha')
    torneo = request.GET.get('torneo')
    producto = request.GET.get('producto')


    if fecha:
        ventas = ventas.filter(fecha__date=fecha)

    if torneo:
        ventas = ventas.filter(torneo__nombre__icontains=torneo)        

    if producto:
        ventas = ventas.filter(
        detalleventa__producto__nombre__icontains=producto
    ).distinct()

    return render(request, "inventario/lista_ventas.html", {
        "ventas": ventas
    })
    
@login_required
@solo_empleados
def detalle_venta(request, venta_id):

    venta = Venta.objects.get(id=venta_id)

    detalles = DetalleVenta.objects.filter(venta=venta)

    return render(request, "inventario/detalle_venta.html", {
        "venta": venta,
        "detalles": detalles
    })
    
@login_required
@solo_empleados
@transaction.atomic
def eliminar_venta(request, venta_id):

    venta = Venta.objects.get(id=venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta)

    for d in detalles:
        producto = d.producto
        producto.stock += d.cantidad
        producto.save()

    venta.delete()

    from django.contrib import messages
    messages.success(request, "Venta eliminada y stock restaurado correctamente")

    return redirect("/ventas/")

@login_required
@solo_empleados
def exportar_excel(request):

    ventas = Venta.objects.all().order_by('-fecha')

    fecha = request.GET.get('fecha')
    torneo = request.GET.get('torneo')
    producto = request.GET.get('producto')
    
    if fecha:
        ventas = ventas.filter(fecha__date=fecha)

    if torneo:
        ventas = ventas.filter(torneo__nombre__icontains=torneo)

    if producto:
        ventas = ventas.filter(
        detalleventa__producto__nombre__icontains=producto
    ).distinct()
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Reporte de Ventas"

    ws.append([
        "ID Venta",
        "Empleado",
        "Torneo",
        "Producto",
        "Cantidad",
        "Precio",
        "Subtotal",
        "Total Venta",
        "Fecha"
    ])

    for venta in ventas:

        detalles = DetalleVenta.objects.filter(venta=venta)

        for d in detalles:
            ws.append([
                venta.id,
                venta.empleado.username,
                venta.torneo.nombre if venta.torneo else "Venta normal",
                d.producto.nombre,
                d.cantidad,
                float(d.precio),
                float(d.subtotal),
                float(venta.total),
                str(venta.fecha)
            ])
            for cell in ws[1]:
                cell.font = Font(bold=True)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = "attachment; filename=reporte_ventas.xlsx"
    for column in ws.columns:
        max_length = 0
    col = column[0].column_letter

    for cell in column:
        try:
            if len(str(cell.value)) > max_length:
                max_length = len(str(cell.value))
        except:
            pass

    ws.column_dimensions[col].width = max_length + 2
    wb.save(response)

    return response

@login_required
@solo_empleados
def reporte_pdf(request):

    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, Spacer
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet
    from django.http import HttpResponse
    import os
    from django.conf import settings

    ventas = Venta.objects.all().order_by('-fecha')

    fecha = request.GET.get('fecha')
    torneo = request.GET.get('torneo')
    producto = request.GET.get('producto')

    if fecha:
        ventas = ventas.filter(fecha__date=fecha)

    if torneo:
        ventas = ventas.filter(torneo__nombre__icontains=torneo)

    if producto:
        ventas = ventas.filter(
            detalleventa__producto__nombre__icontains=producto
        ).distinct()

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=reporte_ventas.pdf"

    doc = SimpleDocTemplate(response, pagesize=letter)

    elements = []
    styles = getSampleStyleSheet()

    logo_path = os.path.join(settings.BASE_DIR, 'static/IMG/logo.jpg')
    if os.path.exists(logo_path):
        elements.append(Image(logo_path, width=80, height=80))

    elements.append(Paragraph("REPORTE DE VENTAS - LiquorEvents", styles['Title']))
    elements.append(Spacer(1, 10))

    if fecha:
        elements.append(Paragraph(f"Fecha: {fecha}", styles['Normal']))
    if torneo:
        elements.append(Paragraph(f"Torneo: {torneo}", styles['Normal']))
    if producto:
        elements.append(Paragraph(f"Producto: {producto}", styles['Normal']))

    elements.append(Spacer(1, 10))

    data = [
        ["ID", "Empleado", "Torneo", "Producto", "Cant", "Subtotal"]
    ]

    total_general = 0

    for venta in ventas:

        detalles = DetalleVenta.objects.filter(venta=venta)

        for d in detalles:
            data.append([
                venta.id,
                venta.empleado.username,
                venta.torneo.nombre if venta.torneo else "Normal",
                d.producto.nombre,
                d.cantidad,
                f"${int(d.subtotal)}"
            ])

            total_general += d.subtotal

    table = Table(data)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),

        ('GRID', (0,0), (-1,-1), 1, colors.black),

        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (4,1), (5,-1), 'CENTER'),
    ]))

    elements.append(table)

    elements.append(Spacer(1, 15))

    elements.append(Paragraph(f"TOTAL GENERAL: ${int(total_general)}", styles['Heading2']))

    doc.build(elements)

    return response