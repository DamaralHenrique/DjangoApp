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