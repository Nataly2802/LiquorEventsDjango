from django.shortcuts import render
from .models import Torneo
# Create your views here.
def lista_torneos(request):
    torneos = Torneo.objects.all()
    return render(request, "torneos/lista.html", {
        "torneos": torneos
    })