import datetime

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.shortcuts import render
from .forms import ReportForm
from django.contrib import messages


# from flight.forms import DataFormr

# VIEWS INICIAIS 
def loginViews(request):
    return render(request, "login.html")

def telaInicialViews(request):
    return render(request, "tela_inicial.html")


# RELATORIO
def telaGerarRelatorioViews(request):

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = ReportForm(request.POST)
        context = {
            'form': form,
        }

        initial_date = request.POST['initial_date']
        final_date = request.POST['final_date']

        if initial_date > datetime.date.today():
            print('Data inicial maior que a atual!')
            

        if final_date > datetime.date.today():
            print('Data final maior que a atual!')
            
        if initial_date >= final_date:
            print('Data inicial maior que a fina!')

        # Check if the form is valid:
        if form.is_valid():
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('menu'))
        else:
            messages.warning(request, 'Erro nos campos!')

    # If this is a GET (or any other method) create the default form
    else:
        context ={}
        context['form']= ReportForm()

    return render(request, "relatorio_gerar.html", context)

def telaPreviewRelatorioViews(request):
    return render(request, "relatorio_preview.html")


# MONITORAMENTO
def telaPainelMonitoramentoViews(request):
    return render(request, "monitoramento_painel.html")

def telaMonitoramentoViews(request):
    return render(request, "monitoramento_voo.html")

def telaAtualizarMonitoramentoViews(request):
    return render(request, "monitoramento_atualizacao.html")


# CRUD VOOS
def telaListaVoosViews(request):
    return render(request, "voo_lista.html")

def telaCreateVooViews(request):
    return render(request, "voo_c.html")

def telaUpdateVooViews(request):
    return render(request, "voo_u.html")
    
def telaReadDeleteVooViews(request):
    return render(request, "voo_rd.html")