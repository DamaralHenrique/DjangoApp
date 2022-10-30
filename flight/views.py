import datetime

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.shortcuts import render

from flight.forms import DataForm

# VIEWS INICIAIS 
def loginViews(request):
    return render(request, "login.html")

def telaInicialViews(request):
    return render(request, "tela_inicial.html")


# RELATORIO
def telaGerarRelatorioViews(request):

    voo_instance = get_object_or_404(VooInstance, pk=pk)


    if request.method == 'POST':

        form = DataForm(request.POST)


        if form.is_valid():
            voo_instance.due_back = form.cleaned_data['renewal_date']
            voo_instance.save()
            return HttpResponseRedirect(reverse('all-borrowed'))

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = DataForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'voo_instance': voo_instance,
    }

    return render(request, "relatorio_gerar.html")

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