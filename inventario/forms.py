from django import forms
from .models import Producto


class VentaForm(forms.Form):

    producto = forms.ModelChoiceField(
        queryset=Producto.objects.all()
    )

    cantidad = forms.IntegerField(min_value=1)