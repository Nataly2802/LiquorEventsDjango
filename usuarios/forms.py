from django import forms
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm


class RegistroParticipanteForm(UserCreationForm):

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = 'participante'
        if commit:
            user.save()
        return user