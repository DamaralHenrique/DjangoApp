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
    ('6', 'Rota 6 (Salvados -> Guarulhos)'),
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

