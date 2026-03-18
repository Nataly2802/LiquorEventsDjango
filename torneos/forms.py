from django import forms
from .models import Torneo

class TorneoForm(forms.ModelForm):
    class Meta:
        model = Torneo
        fields = ['nombre', 'descripcion', 'fecha', 'cupo_maximo']