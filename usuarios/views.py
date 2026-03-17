from django.shortcuts import render, redirect
from .forms import RegistroParticipanteForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView

def registro(request):

    if request.method == 'POST':
        form = RegistroParticipanteForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Usuario registrado correctamente")
            return redirect('lista_torneos')

    else:
        form = RegistroParticipanteForm()

    return render(request, 'usuarios/registro.html', {
        'form': form
    })
    
def cerrar_sesion(request):
    logout(request)
    messages.info(request, "Sesión cerrada correctamente")
    return redirect('lista_torneos')

class CustomLoginView(LoginView):
    
    template_name = 'usuarios/login.html'

    def form_valid(self, form):
        messages.success(self.request, "Bienvenido al sistema")
        return super().form_valid(form)