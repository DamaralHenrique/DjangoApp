import datetime

from django.shortcuts import get_object_or_404, render
from .forms import ReportForm
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.template import loader

from .forms import *
from .models import *

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
    # createDummyData() # DESCOMENTAR PARA CRIAR OS DADOS

    voos = Voo.objects.all().values()
    template = loader.get_template('voo_lista.html')
    context = {
        'voos': voos,
    }
    return HttpResponse(template.render(context, request))


def telaCreateVooViews(request):
    
    if request.method == 'POST':
        form = UpdateVoo(request.POST)

        if form.is_valid():
            return HttpResponseRedirect(reverse('lista_de_voos'))

    # GET
    else:
        previsao_de_partida = datetime.date.today() # numero da partida atual do banco de dados
        form = UpdateVoo(initial={'partida_prevista': previsao_de_partida})
    
    context ={}
    context['form_create_voo']= CreateVoo()
    return render(request, "voo_c.html", context)


def telaUpdateVooViews(request, id):
    
    if request.method == 'POST':
        form = UpdateVoo(request.POST)

        if form.is_valid():
            return HttpResponseRedirect(reverse('read_or_delete'))

    # GET
    else:
        previsao_de_partida = datetime.date.today() # numero da partida atual do banco de dados
        form = UpdateVoo(initial={'partida_prevista': previsao_de_partida})

    context = {}
    context['form_update_voo']= UpdateVoo()
    context['id_voo'] = id
    template = loader.get_template('voo_u.html')
    return HttpResponse(template.render(context, request))

    # return render(request, "voo_u.html", context)


def telaReadDeleteVooViews(request, id):
    template = loader.get_template('voo_rd.html')
    context = {
        'voo': Voo.objects.get(id=id),
    }
    return HttpResponse(template.render(context, request))


# MONITORAMENTO DE VOOS DINAMICOS
def telaMonitoramentoPainel(request):
    # CRIAR UM createDummyData() PARA O BANCO DE DADOS

    voosDinamicos = VooDinamico.objects.all().values()
    template = loader.get_template('monitoramento_painel.html')
    context = {
        'voosDinamicos': voosDinamicos,
    }
    return HttpResponse(template.render(context, request))


def telaMonitoramentoVoo(request, id):
    template = loader.get_template('monitoramento_voo.html')
    context = {
        'vooDinamico': VooDinamico.objects.get(id=id),
    }
    return HttpResponse(template.render(context, request))


def telaMonitoramentoAtualizacao(request, id):
    
    if request.method == 'POST':
        #form = UpdateVoo(request.POST)

        if form.is_valid():
            # TO DO: fazer o update
            return HttpResponseRedirect(reverse('painel_monitoracao'))

    # GET
    else:
        # previsao_de_partida = datetime.date.today() # 
        # form = UpdateVoo(initial={'partida_prevista': previsao_de_partida}) # alterar para 

    context = {}
    # context['form_update_voo_Dinamico']= UpdateVooDinamico()
    context['id_voo_dinamico'] = id
    template = loader.get_template('monitoramento_painel.html')
    return HttpResponse(template.render(context, request))


class ControleVoo():
    def __init__(self) -> None:
        pass

def createDummyData():
    StatusVoo.objects.create(titulo="embarcando")
    StatusVoo.objects.create(titulo="cancelado")
    StatusVoo.objects.create(titulo="programado")
    StatusVoo.objects.create(titulo="taxiando")
    StatusVoo.objects.create(titulo="pronto")
    StatusVoo.objects.create(titulo="autorizado")
    StatusVoo.objects.create(titulo="em voo")
    StatusVoo.objects.create(titulo="aterrissando")

    rota1 = Rota.objects.create(id=123, 
                                aeroporto_partida="Aeroporto 1", 
                                aeroporto_chegada="Aeroporto 2")
    Voo.objects.create(id=1234,
                       rota=rota1,
                       chegada_prevista=datetime.datetime(2022, 6, 10, 16, 00),
                       partida_prevista=datetime.datetime(2022, 6, 10, 10, 00),
                       companhia_aerea="Companhia 1")

    rota2 = Rota.objects.create(id=124, 
                                aeroporto_partida="Aeroporto 12", 
                                aeroporto_chegada="Aeroporto 23")
    Voo.objects.create(id=1235,
                       rota=rota2,
                       chegada_prevista=datetime.datetime(2022, 6, 10, 16, 00),
                       partida_prevista=datetime.datetime(2022, 6, 10, 10, 00),
                       companhia_aerea="Companhia 2")
