from django.shortcuts import render, redirect
from .forms import RegistroParticipanteForm


def registro(request):

    if request.method == 'POST':
        form = RegistroParticipanteForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('lista_torneos')

    else:
        form = RegistroParticipanteForm()

    return render(request, 'usuarios/registro.html', {
        'form': form
    })