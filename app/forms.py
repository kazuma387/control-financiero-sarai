from django import forms
from django.forms import DateInput, ModelForm
from .models import Paciente, Consumos

class PacienteForm(ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            'fecha': DateInput(attrs={'type' : 'date'}),
            'telefono': forms.TextInput(attrs={'placeholder': '57'}),
        }

    # para que el campo telefono tenga el valor por defecto 57
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk and not self.data:
            self.initial['telefono'] = '57'


class ConsumosForm(ModelForm):
    class Meta:
        model = Consumos
        fields = '__all__'
        widgets = {
            'fecha': DateInput(attrs={'type' : 'date'}),
        }