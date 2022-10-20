from django.shortcuts import render

# VIEWS INICIAIS 
def loginViews(request):
    return render(request, "login.html")

def telaInicialViews(request):
    return render(request, "tela_inicial.html")


# RELATORIO
def telaGerarRelatorioViews(request):
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