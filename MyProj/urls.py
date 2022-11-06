"""MyProj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from flight import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.loginViews),
    path('home/', views.telaInicialViews, name = 'menu'),
    path('home/monitoramento_painel/', views.telaMonitoramentoPainelViews, name = 'painel_monitoracao'),
    path('home/gerar_relatorio/', views.telaGerarRelatorioViews),
    path('home/gerar_relatorio/preview_relatorio/', views.telaPreviewRelatorioViews),
    path('home/lista_voos/', views.telaListaVoosViews, name = 'lista_de_voos')
]

urlpatterns += [
    path('home/lista_voos/create/', views.telaCreateVooViews),
    path('home/lista_voos/update/<int:id>/', views.telaUpdateVooViews),
    path('home/lista_voos/read_or_delete/<int:id>/', views.telaReadDeleteVooViews, name = 'read_or_delete')
]

urlpatterns += [
    path('home/monitoramento_painel/monitoramento_atualizacao/<int:id>/', views.telaMonitoramentoAtualizacaoViews, name = 'atualizar_voo_monitorado'),
]

urlpatterns += [
    path('home/gerar_relatorio/preview_relatorio/report/', views.report)
]