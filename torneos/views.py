from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Integrante, Torneo, Inscripcion
from .forms import InscripcionForm, TorneoForm
from django.contrib import messages
from django.http import HttpResponseForbidden

def lista_torneos(request):
    
    torneos = Torneo.objects.all()

    inscritos = []

    if request.user.is_authenticated:
        inscritos = Inscripcion.objects.filter(
            participante=request.user
        ).values_list('torneo_id', flat=True)

    for torneo in torneos:
        torneo.total_inscritos = torneo.inscripcion_set.count()
        torneo.cupos_disponibles = torneo.cupo_maximo - torneo.total_inscritos
    
    return render(request, "torneos/lista.html", {
        "torneos": torneos,
        "inscritos": inscritos
    })
    
@login_required
def inscribirse(request, torneo_id):

    torneo = get_object_or_404(Torneo, id=torneo_id)

    if hasattr(torneo, 'estado_reserva') and torneo.estado_reserva == "Cerradas":
        messages.error(request, "Las inscripciones están cerradas")
        return redirect('lista_torneos')

    total_inscritos = torneo.inscripcion_set.count()

    if total_inscritos >= torneo.cupo_maximo:
        if hasattr(torneo, 'estado_reserva'):
            torneo.estado_reserva = "Cerradas"
            torneo.save()

        messages.error(request, "El torneo ya está lleno")
        return redirect('lista_torneos')

    existe = Inscripcion.objects.filter(
        participante=request.user,
        torneo=torneo
    ).exists()

    if existe:
        messages.warning(request, "Ya estás inscrito en este torneo")
        return redirect('lista_torneos')

    tipo = request.GET.get('tipo')

    if not tipo:
        return render(request, "torneos/tipo_inscripcion.html", {
            "torneo": torneo
        })

    if tipo == "individual":
        if request.method == "POST":
            nombre = request.POST.get("nombre")
            celular = request.POST.get("celular")

            Inscripcion.objects.create(
                participante=request.user,
                torneo=torneo,
                nombre_equipo=nombre,
                numero_personas=1,
                categoria=celular
            )

            messages.success(request, "Inscripción individual exitosa")
            return redirect('lista_torneos')

        return render(request, "torneos/individual.html", {
            "torneo": torneo
        })

    if tipo == "equipo":
        if request.method == "POST":
            nombre_equipo = request.POST.get("nombre_equipo")
            numero_personas = int(request.POST.get("numero_personas", 0))

            inscripcion = Inscripcion.objects.create(
                participante=request.user,
                torneo=torneo,
                nombre_equipo=nombre_equipo,
                numero_personas=numero_personas
            )

            for i in range(numero_personas):
                nombre = request.POST.get(f"nombre_{i}")
                celular = request.POST.get(f"celular_{i}")

                if nombre and celular:
                    Integrante.objects.create(
                        inscripcion=inscripcion,
                        nombre=nombre,
                        celular=celular
                    )

            messages.success(request, "Equipo inscrito correctamente")
            return redirect('lista_torneos')

        return render(request, "torneos/equipo.html", {
            "torneo": torneo
        })
@login_required
def mis_torneos(request):

    inscripciones = Inscripcion.objects.filter(
        participante=request.user
    )

    return render(request, "torneos/mis_torneos.html", {
        "inscripciones": inscripciones
    })

@login_required
def crear_torneo(request):

    if request.user.rol == 'participante':
        return HttpResponseForbidden("No tienes permiso para crear torneos")

    if request.method == 'POST':
        form = TorneoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Torneo creado correctamente")
            return redirect('lista_torneos')
    else:
        form = TorneoForm()

    return render(request, 'torneos/crear_torneo.html', {'form': form})
@login_required
def ver_inscritos(request, torneo_id):
    torneo = get_object_or_404(Torneo, id=torneo_id)

    if request.user.rol == 'participante':
        return HttpResponseForbidden("No tienes permiso para ver esto")

    inscritos = torneo.inscripcion_set.all()

    total_personas = 0
    for ins in inscritos:
        if ins.numero_personas:
            total_personas += ins.numero_personas
        else:
            total_personas += 1

    total_recaudado = 0
    for ins in inscritos:
        personas = ins.numero_personas if ins.numero_personas else 1

        if bool(ins.pago):
            total_recaudado += torneo.valor_inscripcion * personas
    print(torneo.valor_inscripcion)
    return render(request, "torneos/inscritos.html", {
        "torneo": torneo,
        "inscritos": inscritos,
        "total_recaudado": total_recaudado,
        "total_personas": total_personas
    })
@login_required
def cancelar_inscripcion(request, torneo_id):

    torneo = get_object_or_404(Torneo, id=torneo_id)

    inscripcion = Inscripcion.objects.filter(
        participante=request.user,
        torneo=torneo
    )

    if inscripcion.exists():
        inscripcion.delete()
        messages.success(request, "Has cancelado tu inscripción")

    else:
        messages.warning(request, "No estabas inscrito en este torneo")

    return redirect('lista_torneos')

@login_required
def editar_torneo(request, torneo_id):

    torneo = get_object_or_404(Torneo, id=torneo_id)

    if request.user.rol == 'participante':
        return HttpResponseForbidden("No tienes permiso para editar torneos")

    if request.method == 'POST':
        form = TorneoForm(request.POST, request.FILES, instance=torneo)
        if form.is_valid():
            form.save()
            messages.success(request, "Torneo actualizado correctamente")
            return redirect('lista_torneos')
    else:
        form = TorneoForm(instance=torneo)

    return render(request, 'torneos/crear_torneo.html', {'form': form})

@login_required
def eliminar_torneo(request, torneo_id):

    torneo = get_object_or_404(Torneo, id=torneo_id)

    if request.user.rol == 'participante':
        return HttpResponseForbidden("No tienes permiso para eliminar torneos")

    torneo.delete()
    messages.success(request, "Torneo eliminado correctamente")

    return redirect('lista_torneos')

def redireccion_login(request):
    if request.user.rol == 'participante':
        return redirect('lista_torneos')
    return redirect('/dashboard')

@login_required
def cambiar_pago(request, inscripcion_id):
    inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id)

    if request.user.rol == 'participante':
        return HttpResponseForbidden("No tienes permiso")

    inscripcion.pago = not inscripcion.pago
    inscripcion.save()

    return redirect('ver_inscritos', torneo_id=inscripcion.torneo.id)
@login_required
def eliminar_participante(request, inscripcion_id):
    inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id)

    if request.user.rol == 'participante':
        return HttpResponseForbidden("No tienes permiso")

    torneo_id = inscripcion.torneo.id
    inscripcion.delete()

    messages.success(request, "Participante eliminado")
    return redirect('ver_inscritos', torneo_id=torneo_id)
@login_required
def seleccionar_ganador(request, torneo_id, inscripcion_id):
    torneo = get_object_or_404(Torneo, id=torneo_id)

    if request.user.rol == 'participante':
        return HttpResponseForbidden("No tienes permiso")

    inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id)

    torneo.ganador = inscripcion
    torneo.save()

    messages.success(request, "Ganador registrado correctamente")

    return redirect('ver_inscritos', torneo_id=torneo.id)