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

        if int(form.data['report_type']) == 1: # 'Movimentação de voos por período'
            if not form.data['initial_date'] or not form.data['final_date']:
                messages.warning(request, 'Campos "Initail date" e "Final date" devem ser preenchidos para este tipo de relatório!')
            else:
                date_format = "%Y-%m-%d"
                initial_date = datetime.datetime.strptime(request.POST['initial_date'], date_format)
                final_date = datetime.datetime.strptime(request.POST['final_date'], date_format)

                if initial_date.date() > datetime.date.today():
                    messages.warning(request, 'Data inicial maior que a atual!')
                
                # elif final_date.date() > datetime.date.today():
                #     messages.warning(request, 'Data final maior que a atual!')

                elif initial_date.date() >= final_date.date():
                    messages.warning(request, 'Data inicial maior que a final!')

                else:
                    # Pegar tabela com cada um desses voos
                    voos_partidas = VooDinamico.objects.all().filter(partida_real__gte=initial_date, partida_real__lte=final_date)
                    voos_chegadas = VooDinamico.objects.all().filter(partida_real__gte=initial_date, partida_real__lte=final_date)

                    # Pegar numero de voos que chegaram e que partiram em um periodo
                    num_partidas = voos_partidas.count()
                    num_chegadas = voos_chegadas.count()

                    context = {"voos_partidas": voos_partidas,
                               "voos_chegadas": voos_chegadas,
                               "num_partidas": num_partidas,
                               "num_chegadas": num_chegadas}

                    voo_data_partida = []
                    voo_data_chegada = []

                    for voo in voos_partidas:
                        voo_data = {
                            "Companhia Aérea": voo.voo.companhia_aerea,
                            "Voo": voo.voo.id,
                            "Destino": voo.voo.rota.aeroporto_chegada,
                            "Partida Prevista": voo.voo.partida_prevista.strftime("%m/%d/%Y, %H:%M:%S"),
                            "Partida Real": voo.partida_real.strftime("%m/%d/%Y, %H:%M:%S")
                        }
                        voo_data_partida.append(voo_data)
                    
                    for voo in voos_chegadas:
                        voo_data = {
                            "Companhia Aérea": voo.voo.companhia_aerea,
                            "Voo": voo.voo.id,
                            "Origem": voo.voo.rota.aeroporto_partida,
                            "Chegada Prevista": voo.voo.chegada_prevista.strftime("%m/%d/%Y, %H:%M:%S"),
                            "Chegada Real": voo.chegada_real.strftime("%m/%d/%Y, %H:%M:%S")
                        }
                        voo_data_chegada.append(voo_data)

                    test_context = {
                        "voos_partida": voo_data_partida,
                        "voos_chegada": voo_data_chegada,
                        "num_partidas": num_partidas,
                        "num_chegadas": num_chegadas,
                        "data_inicial": request.POST['initial_date'],
                        "data_final": request.POST['final_date'],
                        "voo_data_companhia": ""
                    }

                    request.session['report_context'] = test_context
                    return render(request, "relatorio_preview.html", context)

        else: # 'Partidas e chegadas por empresas'
            companhias_aereas = ["GOL", "LATAM", "AZUL"]
            voo_data = []
            for companhia_aerea in companhias_aereas:

                voos = VooDinamico.objects.all().filter(voo__companhia_aerea=companhia_aerea)
                num_voos = voos.count()

                voo_data_companhia = {
                    "companhia_aerea": companhia_aerea,
                    "num_voos": num_voos
                }
                voo_data.append(voo_data_companhia)
                
            session_data = {
                "voos_partida": "",
                "voos_chegada": "",
                "num_partidas": "",
                "num_chegadas": "",
                "data_inicial": "",
                "data_final": "",
                "voo_data_companhia": voo_data
            }
            context = {"voo_data_companhia": voo_data}
            request.session['report_context'] = session_data
            return render(request, "relatorio_preview.html", context)

    template = loader.get_template('relatorio_gerar.html')

    context ={}
    context['form']= ReportForm()

    return HttpResponse(template.render(context, request))


def telaPreviewRelatorioViews(request):
    context ={}
    return render(request, "relatorio_preview.html", context)

def report(request):
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    voo_data = request.session.get('report_context')
    if not voo_data["voo_data_companhia"]: # Relatório de Movimentação de voos
        voos_partida = voo_data["voos_partida"]
        voos_chegada = voo_data["voos_chegada"]
        num_partidas = voo_data["num_partidas"]
        num_chegadas = voo_data["num_chegadas"]
        data_inicial = voo_data["data_inicial"]
        data_final = voo_data["data_final"]

        pdf.set_font('courier', 'B', 16)
        pdf.cell(40, 10, 'Movimentação de voos',0,1)
        pdf.cell(100, 10, '',0,1)

        # Datas
        pdf.set_font('courier', '', 12)
        pdf.cell(40, 10, 'Data inicial: ' + data_inicial,0,1)
        pdf.cell(40, 10, 'Data final: ' + data_final,0,1)

        # Partidas
        pdf.cell(40, 10, 'Número de partidas: ' + str(num_partidas),0,1)

        pdf.set_font('courier', 'B', 8)
        pdf.cell(1000, 8, f"{'Companhia Aérea'.ljust(20)} {'Voo'.ljust(10)} {'Destino'.ljust(20)} {'Partida prevista'.ljust(30)} {'Partida real'.ljust(10)}", 0, 1)
        # pdf.line(10, 40, 200, 40)
        # pdf.line(10, 48, 200, 48)
        pdf.set_font('courier', '', 8)
        for line in voos_partida:
            pdf.cell(1000, 8, f"{line['Companhia Aérea'].ljust(20)} {str(line['Voo']).ljust(10)} {line['Destino'].ljust(20)} {line['Partida Prevista'].ljust(30)} {line['Partida Real'].ljust(10)}", 0, 1)

        # Chegadas
        pdf.set_font('courier', '', 12)
        pdf.cell(40, 10, 'Número de chegadas: ' + str(num_chegadas),0,1)

        pdf.set_font('courier', 'B', 8)
        pdf.cell(1000, 8, f"{'Companhia Aérea'.ljust(20)} {'Voo'.ljust(10)} {'Origem'.ljust(20)} {'Chegada prevista'.ljust(30)} {'Chegada real'.ljust(10)}", 0, 1)
        # pdf.line(10, 30, 200, 30)
        # pdf.line(10, 38, 200, 38)
        pdf.set_font('courier', '', 8)
        for line in voos_chegada:
            pdf.cell(1000, 8, f"{line['Companhia Aérea'].ljust(20)} {str(line['Voo']).ljust(10)} {line['Origem'].ljust(20)} {line['Chegada Prevista'].ljust(30)} {line['Chegada Real'].ljust(10)}", 0, 1)

    else: # Relatório de voos por companhia
        voo_data_companhia = voo_data["voo_data_companhia"]

        pdf.set_font('courier', 'B', 16)
        pdf.cell(40, 10, 'Número de voos por companhia',0,1)
        pdf.cell(100, 10, '',0,1)
        
        for line in voo_data_companhia:
            pdf.cell(1000, 8, f"{line['companhia_aerea'].ljust(20)} {str(line['num_voos']).ljust(10)}", 0, 1)

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