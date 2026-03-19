from django import forms
from .models import Torneo

class TorneoForm(forms.ModelForm):
    class Meta:
        model = Torneo
        fields = [
    'nombre',
    'descripcion',
    'fecha',
    'hora',
    'cupo_maximo',
    'premio',
    'tipo_juego',
    'estado_reserva',
    'imagen'
]
        widgets = {
            'fecha': forms.DateInput(
                format='%Y-%m-%d', 
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'hora': forms.TimeInput(attrs={'type': 'time'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.fecha:
            self.initial['fecha'] = self.instance.fecha.strftime('%Y-%m-%d')
    def clean_cupo_maximo(self):
        cupo = self.cleaned_data.get('cupo_maximo')
        if cupo <= 0:
            raise forms.ValidationError("El cupo debe ser mayor a 0")
        return cupo