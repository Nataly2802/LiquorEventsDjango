from django.shortcuts import render

# Create your views here.
def lista_torneos(request):
    return render(request, "torneos/lista.html")