from django import forms
from .models import Producto


class VentaForm(forms.Form):

    class VentaForm(forms.Form):
        producto = forms.ModelChoiceField(
        queryset=Producto.objects.all()
    )

    cantidad = forms.IntegerField(min_value=1)

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'codigo',
            'nombre',
            'marca',
            'categoria',
            'precio',
            'stock',
            'imagen',
            'descripcion'
        ]