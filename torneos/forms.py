from django import forms
from .models import Torneo

class TorneoForm(forms.ModelForm):
    class Meta:
        model = Torneo
        fields = ['nombre', 'descripcion', 'fecha', 'cupo_maximo', 'imagen']
        widgets = {
            'fecha': forms.DateInput(
                format='%Y-%m-%d', 
                attrs={'type': 'date', 'class': 'form-control'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.fecha:
            self.initial['fecha'] = self.instance.fecha.strftime('%Y-%m-%d')
