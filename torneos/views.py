from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Torneo, Inscripcion
# Create your views here.
def lista_torneos(request):
    torneos = Torneo.objects.all()
    return render(request, "torneos/lista.html", {
        "torneos": torneos
    })
    
@login_required
def inscribirse(request, torneo_id):

    torneo = get_object_or_404(Torneo, id=torneo_id)

    Inscripcion.objects.create(
        participante=request.user,
        torneo=torneo
    )

    return redirect('lista_torneos')