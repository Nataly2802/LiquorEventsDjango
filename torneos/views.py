from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Torneo, Inscripcion
# Create your views here.
def lista_torneos(request):
    
    torneos = Torneo.objects.all()

    inscritos = []

    if request.user.is_authenticated:
        inscritos = Inscripcion.objects.filter(
            participante=request.user
        ).values_list('torneo_id', flat=True)

    return render(request, "torneos/lista.html", {
        "torneos": torneos,
        "inscritos": inscritos
    })
    
@login_required
def inscribirse(request, torneo_id):

    torneo = get_object_or_404(Torneo, id=torneo_id)

    # verificar si ya está inscrito
    existe = Inscripcion.objects.filter(
        participante=request.user,
        torneo=torneo
    ).exists()

    if not existe:

        Inscripcion.objects.create(
            participante=request.user,
            torneo=torneo
        )

    return redirect('lista_torneos')

@login_required
def mis_torneos(request):

    inscripciones = Inscripcion.objects.filter(
        participante=request.user
    )

    return render(request, "torneos/mis_torneos.html", {
        "inscripciones": inscripciones
    })
