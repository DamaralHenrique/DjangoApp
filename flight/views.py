import datetime

import pytz
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.urls import reverse
from django.template import loader
from fpdf import FPDF

from .forms import *
from .models import *

login_limit = 0

class User:
  def __init__(self, id, name, password, post):
    self.id = id
    self.name = name
    self.password = password
    self.post = post

LOGINS = [
    User("operador","Milenha","qwer",1),
    User("funcionario","Arthur","qwer",2),
    User("gerente","Juliano","qwer",3)
]

# VIEWS INICIAIS 
def loginViews(request):
    global login_limit
    global LOGINS
    context ={}
    if request.method == 'POST':
        if(login_limit == 2):
            context['WarningMessage']= "Você atingiu o limite de 3 tentativas"
        else:
            user_id = request.POST['user_id']
            password = request.POST['password']

            user = next((x for x in LOGINS if (x.id == user_id and x.password == password)), None)

            if(user == None):
                login_limit = login_limit + 1
                context['WarningMessage']= "Login ou senha incorretos"
                context['form']= LoginForm()
            else:
                login_limit = 0
                return HttpResponseRedirect(reverse('menu', kwargs={'post':int(user.post)}))
    else:
        context['form']= LoginForm()
    return render(request, "login.html", context)

def telaInicialViews(request, post):
    context ={}
    context['post']= post
    return render(request, "tela_inicial.html", context)

# RELATORIO
def telaGerarRelatorioViews(request):
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = ReportForm(request.POST)
        context = {
            'form': form,
        }

        date_format = "%Y-%m-%d"
        initial_date = datetime.datetime.strptime(request.POST['initial_date'], date_format)
        final_date = datetime.datetime.strptime(request.POST['final_date'], date_format)

        if initial_date.date() > datetime.date.today():
            print('Data inicial maior que a atual!')
            
        if final_date.date() > datetime.date.today():
            print('Data final maior que a atual!')

        if initial_date.date() >= final_date.date():
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
    context ={}
    return render(request, "relatorio_preview.html", context)

def report(request):
    sales = [
        {"item": "Keyboard", "amount": "$120,00"},
        {"item": "Mouse", "amount": "$10,00"},
        {"item": "House", "amount": "$1 000 000,00"},
    ]
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('courier', 'B', 16)
    pdf.cell(40, 10, 'This is what you have sold this month so far:',0,1)
    pdf.cell(40, 10, '',0,1)
    pdf.set_font('courier', '', 12)
    pdf.cell(200, 8, f"{'Item'.ljust(30)} {'Amount'.rjust(20)}", 0, 1)
    pdf.line(10, 30, 150, 30)
    pdf.line(10, 38, 150, 38)
    for line in sales:
        pdf.cell(200, 8, f"{line['item'].ljust(30)} {line['amount'].rjust(20)}", 0, 1)

    pdf.output('report.pdf', 'F')
    
    return FileResponse(open('report.pdf', 'rb'), as_attachment=True, content_type='application/pdf')

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
        form = CreateVoo(request.POST)

        if form.is_valid():
            voo_obj = Voo.objects.create(
                rota = Rota.objects.get(id=form.data['rota']),
                chegada_prevista = form.data['previsao_de_chegada'],
                partida_prevista = form.data['previsao_de_partida'],
                companhia_aerea = form.data['companhia_aerea'],
            )

            VooDinamico.objects.create(
                voo=voo_obj,
                status=StatusVoo.objects.get(titulo="-"),
                partida_real=None,
                chegada_real=None
            )

            return HttpResponseRedirect(reverse('lista_de_voos'))
    
    context ={}
    context['form_create_voo']= CreateVoo()
    return render(request, "voo_c.html", context)

def telaUpdateVooViews(request, id):
    if request.method == 'POST':
        form = UpdateVoo(request.POST)

        if form.is_valid():
            Voo.objects.all().filter(id=id).update(rota=Rota.objects.get(id=form.data['rota']),
                                                   partida_prevista=form.data['previsao_de_partida'],
                                                   chegada_prevista=form.data['previsao_de_chegada'], 
                                                   companhia_aerea=form.data['companhia_aerea'])
            return HttpResponseRedirect(reverse('read_or_delete', kwargs={'id':int(id)}))

    else:
        previsao_de_partida = datetime.date.today() # numero da partida atual do banco de dados
        form = UpdateVoo(initial={'partida_prevista': previsao_de_partida})

    context = {}
    context['form_update_voo']= UpdateVoo()
    context['id_voo'] = id
    template = loader.get_template('voo_u.html')
    return HttpResponse(template.render(context, request))
    

def telaReadDeleteVooViews(request, id):
    template = loader.get_template('voo_rd.html')
    context = {
        'voo': Voo.objects.get(id=id),
    }

    if request.method == 'POST':
        Voo.objects.all().filter(id=id).delete()
        return HttpResponseRedirect(reverse('lista_de_voos'))

    return HttpResponse(template.render(context, request))

# MONITORAMENTO DE VOOS DINAMICOS
def telaMonitoramentoPainelViews(request):
    voosDinamicos = VooDinamico.objects.all()
    template = loader.get_template('monitoramento_painel.html')
    date = datetime.date.today()
    tz = pytz.timezone('America/Sao_Paulo')
    now = datetime.datetime.now(tz)
    time = now.strftime("%H:%M:%S")
    context = {
        'voosDinamicos': voosDinamicos,
        'time': time,
        'date': date,
    }
    return HttpResponse(template.render(context, request))

def telaMonitoramentoAtualizacaoViews(request, id):
    if request.method == 'POST':
        form = UpdateVooDinamicoStatus(request.POST)

        if form.is_valid():
            current_status_id = VooDinamico.objects.all().filter(voo=id).values_list('status')[0][0]
            new_status_id = int(form.data['status'])

            if not is_new_status_valid(current_status_id, new_status_id):
                print(is_new_status_valid(current_status_id, new_status_id))
                messages.info(request, 'Novo status inválido!')
            
            else:
                tz = pytz.timezone('America/Sao_Paulo')
                VooDinamico.objects.all().filter(voo=id).update(status=StatusVoo.objects.get(id=form.data['status']))
                if new_status_id == 7:
                    VooDinamico.objects.all().filter(voo=id).update(partida_real=datetime.datetime.now(tz))
                elif new_status_id == 8:
                    VooDinamico.objects.all().filter(voo=id).update(chegada_real=datetime.datetime.now(tz))
            
                return HttpResponseRedirect(reverse('painel_monitoracao'))

    context = {
        'vooDinamico': VooDinamico.objects.get(voo_id=id),
    }
    # context['form_update_voo_Dinamico']= UpdateVooDinamico()
    context['id_voo_dinamico'] = id
    context['form_update_voo_status']= UpdateVooDinamicoStatus()
    template = loader.get_template('monitoramento_atualizacao.html')
    return HttpResponse(template.render(context, request))


def is_new_status_valid(current_status, new_status):
    # Legenda:
    # ('1', 'Embarcando'),
    # ('2', 'Cancelado'),
    # ('3', 'Programado'),
    # ('4', 'Taxiando'),
    # ('5', 'Pronto'),
    # ('6', 'Autorizado'),
    # ('7', 'Em voo'),
    # ('8', 'Aterrissando'),
    # ('9', '-'),

    # Embarcando -> Programado
    if current_status == 1 and new_status != 3:
        return False
    
    # - -> Cancelado ou Embarcando
    if current_status == 9 and new_status not in (1, 2):
        return False
    
    # Programado -> Taxiando -> Pronto -> Autorizado -> Em voo -> Aterrisando
    if 3 <= current_status <= 8  and new_status != current_status + 1:
        return False

    if current_status == 2:
        return False

    return True

class ControleVoo():
    def __init__(self) -> None:
        pass

def createDummyData():
    # StatusVoo.objects.create(titulo="embarcando")
    # StatusVoo.objects.create(titulo="cancelado")
    # StatusVoo.objects.create(titulo="programado")
    # StatusVoo.objects.create(titulo="taxiando")
    # StatusVoo.objects.create(titulo="pronto")
    # StatusVoo.objects.create(titulo="autorizado")
    # StatusVoo.objects.create(titulo="em voo")
    # StatusVoo.objects.create(titulo="aterrissando")

    # rota1 = Rota.objects.create(id=123, 
    #                             aeroporto_partida="Aeroporto 1", 
    #                             aeroporto_chegada="Aeroporto 2")
    # Voo.objects.create(id=1234,
    #                    rota=rota1,
    #                    chegada_prevista=datetime.datetime(2022, 6, 10, 16, 00),
    #                    partida_prevista=datetime.datetime(2022, 6, 10, 10, 00),
    #                    companhia_aerea="Companhia 1")

    # rota2 = Rota.objects.create(id=124, 
    #                             aeroporto_partida="Aeroporto 12", 
    #                             aeroporto_chegada="Aeroporto 23")
    # Voo.objects.create(id=1235,
    #                    rota=rota2,
    #                    chegada_prevista=datetime.datetime(2022, 6, 10, 16, 00),
    #                    partida_prevista=datetime.datetime(2022, 6, 10, 10, 00),
    #                    companhia_aerea="Companhia 2")

    # Rota.objects.create(id=1, 
    #                     aeroporto_partida="Guarulhos", 
    #                     aeroporto_chegada="Santos Dumont")
    # Rota.objects.create(id=2, 
    #                     aeroporto_partida="Guarulhos", 
    #                     aeroporto_chegada="Salvador")
    # Rota.objects.create(id=3, 
    #                     aeroporto_partida="Congonhas", 
    #                     aeroporto_chegada="Brasília")
    # Rota.objects.create(id=4, 
    #                     aeroporto_partida="Brasília", 
    #                     aeroporto_chegada="Congonhas")
    pass