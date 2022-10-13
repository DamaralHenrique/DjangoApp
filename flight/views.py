from django.shortcuts import render

# Create your views here.
def loginViews(request):
    return render(request, "login.html")

def telaInicialViews(request):
    return render(request, "tela_inicial.html")

def telaGerarRelatorioViews(request):
    return render(request, "gerar_relatorio.html")

def telaPreviewRelatorioViews(request):
    return render(request, "preview_relatorio.html")

def telaPainelMonitoramentoViews(request):
    return render(request, "monitoramento_painel.html")

def telaMonitoramentoViews(request):
    return render(request, "monitoramento_voo.html")

def telaAtualizarMonitoramentoViews(request):
    return render(request, "monitoramento_atualizacao.html")

def telaListaVoosViews(request):
    return render(request, "lista_voos.html")

def telaCreateVooViews(request):
    return render(request, "c_voo.html")

def telaUpdateVooViews(request):
    return render(request, "u_voo.html")
    
def telaReadDeleteVooViews(request):
    return render(request, "rd_voo.html")