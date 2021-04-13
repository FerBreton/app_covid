from django import forms
from .models import *

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = '__all__'
        exclude = ['estado', 'timestamp_out']

class ResultadoForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = '__all__'
        exclude = ['timestamp_out', 'temperatura', 'oxigenacion', 'estado']