from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Torneo, Inscripcion
from .forms import TorneoForm
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

    total_inscritos = torneo.inscripcion_set.count()

    if total_inscritos >= torneo.cupo_maximo:
        messages.error(request, "El torneo ya está lleno")
        return redirect('lista_torneos')

    existe = Inscripcion.objects.filter(
        participante=request.user,
        torneo=torneo
    ).exists()

    if existe:
        messages.warning(request, "Ya estás inscrito en este torneo")
        return redirect('lista_torneos')

    Inscripcion.objects.create(
        participante=request.user,
        torneo=torneo
    )

    messages.success(request, "Te has inscrito correctamente")

    return redirect('lista_torneos')

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
        form = TorneoForm(request.POST)
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

    return render(request, "torneos/inscritos.html", {
        "torneo": torneo,
        "inscritos": inscritos
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
        form = TorneoForm(request.POST, instance=torneo)
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


