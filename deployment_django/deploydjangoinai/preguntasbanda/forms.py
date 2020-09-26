from django import forms
from django.core import validators
import pickle
import os
from . import fixdependencia

print("el path del forms es:",os.getcwd())

with open('/home/rafaelortega/Documentos/INAI_consultas/inai_rafaelortegar/deployment_django/deploydjangoinai/static/listado_dep.pkl', 'rb') as f:
    mynewlist = pickle.load(f)

OPCIONES_DEP=mynewlist

class FormName(forms.Form):
    dependencia= forms.CharField(label='¿Para que dependencia es la solicitud?', widget=forms.Select(choices=OPCIONES_DEP))
    nombre = forms.CharField()
    email = forms.EmailField()
    texto_de_la_solicitud = forms.CharField(widget=forms.Textarea)
    botcatcher = forms.CharField(required=False,
                                widget=forms.HiddenInput,
                                validators=[validators.MaxLengthValidator(0)])

    # def clean_botcatcher(self):
    #     botcatcher=self.cleaned_data['botcatcher']
    #     if len(botcatcher)>0:
    #         raise forms.ValidationError('GOTCHA BOT!')
    #     return botcatcher
