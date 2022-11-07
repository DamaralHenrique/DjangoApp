from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime

from django import forms
from django.forms import DateTimeInput

# FORMS: LOGIN
class LoginForm(forms.Form):
    user_id= forms.CharField(label='Id do usuário')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

# FORMS: RELATORIOS
class MyDateInput(forms.widgets.DateInput):
    input_type = 'date'

REPORT_TYPES = [
    ('1', 'Movimentação de voos por período'),
    ('2', 'Partidas e chegadas por empresas'),
    ]

FLIGHT_COMPANIES = [
    ('1', '-'),
    ('2', 'GOL'),
    ('3', 'LATAM'),
    ('4', 'AZUL')
    ]

class MyDateInput(forms.widgets.DateInput):
    input_type = 'date'

class ReportForm(forms.Form):
    report_type= forms.CharField(label='Escolha o tipo de relatório a ser gerado:', 
                                 widget=forms.Select(choices=REPORT_TYPES))
    initial_date = forms.DateField(widget=MyDateInput(), required=False)
    final_date = forms.DateField(widget=MyDateInput(), required=False)
    # companhia_aerea = forms.CharField(label='Companhia aérea:', 
                                    #   widget=forms.Select(choices=FLIGHT_COMPANIES), 
                                    #   required=False)

FLIGHT_COMPANY = [
    ('1', 'Companhia 1'),
    ('2', 'Companhia 2'),
    ('3', 'Companhia 3'),
    ('4', 'Companhia 4'),
    ('5', 'Companhia 5'),
]

FLIGHT_TYPES = [
    ('1', 'Tipo 1'),
    ('2', 'Tipo 2'),
    ('3', 'Tipo 3'),
    ('4', 'Tipo 4'),
    ('5', 'Tipo 5'),
]

class ReportCompanyForm(forms.Form):
    flight_company= forms.CharField(label='Companhia aérea:', widget=forms.Select(choices=FLIGHT_COMPANY))
    flight_type= forms.CharField(label='Tipo de voo:', widget=forms.Select(choices=FLIGHT_TYPES))
    

# FORMS: CRUD
ROTAS= [
    ('1', 'Rota 1'),
    ('2', 'Rota 2'),
    ('3', 'Rota 3'),
    ('4', 'Rota 4'),
    ]

class CreateVoo(forms.Form):
    companhia_aerea = forms.CharField(max_length = 200)
    rota= forms.CharField(label='Rota do voo:', widget=forms.Select(choices=ROTAS))
    # local_de_partida = forms.CharField(max_length = 200)
    # local_de_destino = forms.CharField(max_length = 200)
    previsao_de_partida = forms.DateTimeField(widget=DateTimeInput(attrs={'type': 'datetime-local'}))
    previsao_de_chegada = forms.DateTimeField(widget=DateTimeInput(attrs={'type': 'datetime-local'}))

class UpdateVoo(forms.Form):
    companhia_aerea = forms.CharField(max_length = 200)
    rota= forms.CharField(label='Rota do voo:', widget=forms.Select(choices=ROTAS))
    # local_de_partida = forms.CharField(max_length = 200)
    # local_de_destino = forms.CharField(max_length = 200)
    previsao_de_partida = forms.DateTimeField(widget=DateTimeInput(attrs={'type': 'datetime-local'}))
    previsao_de_chegada = forms.DateTimeField(widget=DateTimeInput(attrs={'type': 'datetime-local'}))


# FORMS: MONITORAMENTO
FLIGHT_STATUS = [
    ('1', 'Embarcando'),
    ('2', 'Cancelado'),
    ('3', 'Programado'),
    ('4', 'Taxiando'),
    ('5', 'Pronto'),
    ('6', 'Autorizado'),
    ('7', 'Em voo'),
    ('8', 'Aterrissando')
]

class UpdateVooDinamicoStatus(forms.Form):
    status = forms.CharField(label='Status atualizado:', widget=forms.Select(choices=FLIGHT_STATUS))

