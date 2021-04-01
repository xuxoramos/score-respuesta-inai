from django import forms
from django.core import validators
import pickle
import os
from . import fixdependencia

print("el path del forms de preguntasbanda es:",os.getcwd())

print(os.getcwd()+'/preguntasbanda/static/listado_dep.pkl')

path_este_archivo = os.getcwd()+'/static/listado_dep.pkl'

print(path_este_archivo)

with open(path_este_archivo, 'rb') as f:
    mynewlist = pickle.load(f)

OPCIONES_DEP=mynewlist

class FormName(forms.Form):
    dependencia= forms.CharField(label='¿Para que dependencia es la solicitud?', widget=forms.Select(choices=OPCIONES_DEP))
    texto_de_la_solicitud = forms.CharField(widget=forms.Textarea)
    botcatcher = forms.CharField(required=False,
                                widget=forms.HiddenInput,
                                validators=[validators.MaxLengthValidator(0)])

    # def clean_botcatcher(self):
    #     botcatcher=self.cleaned_data['botcatcher']
    #     if len(botcatcher)>0:
    #         raise forms.ValidationError('GOTCHA BOT!')
    #     return botcatcher
