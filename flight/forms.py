from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime

from django import forms
from django.forms import DateTimeInput

REPORT_TYPES= [
    ('1', 'Movimentação de voos por período'),
    ('2', 'Partidas e chegadas por empresas'),
    ]

class MyDateInput(forms.widgets.DateInput):
    input_type = 'date'
 
# creating a form
class ReportForm(forms.Form):
 
    report_type= forms.CharField(label='Escolha o tipo de relatório a ser gerado', widget=forms.Select(choices=REPORT_TYPES))
    initial_date = forms.DateField(widget=MyDateInput())
    final_date = forms.DateField(widget=MyDateInput())

    def clean_renewal_date(self):
        initial_date = self.data['initial_date']
        final_date = self.data['final_date']

        print(initial_date, final_date)

        # Check if a date is in the allowed range (+4 weeks from today).
        
        if initial_date > datetime.date.today():
            raise ValidationError(_('Data inicial maior que a atual!'))

        if final_date > datetime.date.today():
            raise ValidationError(_('Data final maior que a atual!'))
            
        if initial_date >= final_date:
            raise ValidationError(_('Data inicial maior que a fina!'))

        # Remember to always return the cleaned data.
        return 0



# template (https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms)
class DataForm(forms.Form):
    renewal_date = forms.DateField(
            help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['data_inicio']


        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('Invalid date - renewal more than 4 weeks ahead'))

        return data


class testForm(forms.Form):
    dummyText = forms.CharField(help_text="Enter text")

