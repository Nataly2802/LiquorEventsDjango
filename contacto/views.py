from django.shortcuts import render
from django.shortcuts import render
from django.core.mail import send_mail
from .forms import ContactoForm
from django.core.mail import EmailMessage
# Create your views here.

def contactenos(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            correo = form.cleaned_data['correo']
            asunto = form.cleaned_data['asunto']
            mensaje = form.cleaned_data['mensaje']

            mensaje_completo = f"""
            Nombre: {nombre}
            Correo: {correo}

            Mensaje:
            {mensaje}
            """

            email = EmailMessage(
                asunto,
                mensaje_completo,
                'liquorevents8@gmail.com',
                ['liquorevents8@gmail.com'],
                reply_to=[correo],
            )

            email.send()
            
            respuesta = EmailMessage(
                'Hemos recibido tu mensaje',
                f"""
            Hola {nombre},

            Gracias por contactarnos. Hemos recibido tu mensaje y pronto te responderemos.

            Tu mensaje fue:
            {mensaje}

            Atentamente,
            LiquorEvents
            """,
                'liquorevents8@gmail.com',
                [correo],
            )

            respuesta.send()

            return render(request, 'contacto/contacto.html', {
                'form': ContactoForm(),
                'exito': True
            })
    else:
        form = ContactoForm()

    return render(request, 'contacto/contacto.html', {'form': form})