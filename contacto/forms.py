from django import forms

class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    correo = forms.EmailField()
    asunto = forms.CharField(max_length=150)
    mensaje = forms.CharField(widget=forms.Textarea)