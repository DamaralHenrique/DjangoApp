from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime


from django import forms


ROTAS= [
    ('1', 'Rota 1'),
    ('2', 'Rota 2'),
    ('3', 'Rota 3'),
    ('4', 'Rota 4'),
    ]
# template (https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms)

class CreateVoo(forms.Form):
    numero_do_voo_de_partida = forms.CharField(max_length = 200)
    numero_do_voo_de_chegada = forms.CharField(max_length = 200)
    companhia_aerea = forms.CharField(max_length = 200)
    rota= forms.CharField(label='Rota do voo:', widget=forms.Select(choices=ROTAS))
    local_de_partida = forms.CharField(max_length = 200)
    local_de_destino = forms.CharField(max_length = 200)
    previsao_de_partida = forms.CharField(max_length = 200)
    previsao_de_chegada = forms.CharField(max_length = 200)

class UpdateVoo(forms.Form):
    id_num_partida = forms.CharField(max_length = 200)
    id_num_chegada = forms.CharField(max_length = 200)
    companhia_aerea = forms.CharField(max_length = 200)
    rota= forms.CharField(label='Rota do voo:', widget=forms.Select(choices=ROTAS))
    local_de_partida = forms.CharField(max_length = 200)
    local_de_destino = forms.CharField(max_length = 200)
    previsao_de_partida = forms.CharField(max_length = 200)
    previsao_de_chegada = forms.CharField(max_length = 200)

class testForm(forms.Form):
    dummyText = forms.CharField(help_text="Enter text")

