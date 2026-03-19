from django import forms
from .models import Producto


class VentaForm(forms.Form):

    producto = forms.ModelChoiceField(
        queryset=Producto.objects.filter(estado='Activo')
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
            'estado',
            'descripcion'
        ]