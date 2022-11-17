from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime

from django import forms
from django.forms import DateTimeInput

from .models import *

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

AEROPORTOS= []
aeroportos_partida = list(Rota.objects.all().values_list('aeroporto_partida', flat = True).distinct())
aeroportos_chegada = list(Rota.objects.all().values_list('aeroporto_chegada', flat = True).distinct())


class ReportTypeForm(forms.Form):
    report_type= forms.CharField(label='Escolha o tipo de relatório a ser gerado:', 
                                 widget=forms.Select(choices=REPORT_TYPES))

class ReportAirportForm(forms.Form):
    aeroportos_list = set(aeroportos_partida) | set(aeroportos_chegada)
    for aeroporto_p in aeroportos_list:
        AEROPORTOS.append((aeroporto_p, aeroporto_p))
    aeroporto= forms.CharField(label='Rota do voo:', widget=forms.Select(choices=AEROPORTOS))


class ReportDateForm(forms.Form):
    # report_type= forms.CharField(label='Escolha o tipo de relatório a ser gerado:', 
    #                              widget=forms.Select(choices=REPORT_TYPES))
    
    initial_date = forms.DateField(widget=MyDateInput())
    final_date = forms.DateField(widget=MyDateInput())
    
    # aeroportos_list = set(aeroportos_partida) | set(aeroportos_chegada)
    # for aeroporto_p in aeroportos_list:
    #     AEROPORTOS.append((aeroporto_p, aeroporto_p))
    # aeroporto= forms.CharField(label='Rota do voo:', widget=forms.Select(choices=AEROPORTOS))

    def clean(self):
        initial = self.cleaned_data['initial_date']
        final = self.cleaned_data['final_date']
        if initial > datetime.date.today():
            raise forms.ValidationError("Data inicial maior que a atual!")
                
        elif final > datetime.date.today():
            raise forms.ValidationError("Data final maior que a atual!")

        elif initial >= final:
            raise forms.ValidationError("Data inicial maior que a final!")

        return 0


# FORMS: CRUD
ROTAS= [
    ('1', 'Rota 1 (Guarulhos -> Santos Dumont)'),
    ('2', 'Rota 2 (Santos Dumont -> Guarulhos)'),
    ('3', 'Rota 3 (Guarulhos -> Brasília)'),
    ('4', 'Rota 4 (Brasília -> Guarulhos)'),
    ('5', 'Rota 5 (Guarulhos -> Salvador)'),
    ('6', 'Rota 6 (Salvador -> Guarulhos)'),
]

formatDate = "%Y-%m-%dT%H:%M"

class CreateVoo(forms.Form):
    companhia_aerea = forms.CharField(max_length = 200)
    rota= forms.CharField(label='Rota do voo:', widget=forms.Select(choices=ROTAS))
    previsao_de_partida = forms.DateTimeField(widget=DateTimeInput(attrs={'type': 'datetime-local'}, format=formatDate))
    previsao_de_chegada = forms.DateTimeField(widget=DateTimeInput(attrs={'type': 'datetime-local'}, format=formatDate))


class UpdateVoo(forms.Form):
    companhia_aerea = forms.CharField(max_length = 200)
    rota= forms.CharField(label='Rota do voo:', widget=forms.Select(choices=ROTAS))
    previsao_de_partida = forms.DateTimeField(widget=DateTimeInput(attrs={'type': 'datetime-local'}, format=formatDate))
    previsao_de_chegada = forms.DateTimeField(widget=DateTimeInput(attrs={'type': 'datetime-local'}, format=formatDate))


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
