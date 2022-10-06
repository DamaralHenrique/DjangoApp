from django.db import models

class StatusVoo(models.Model):
    id = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=200,null=False)
    class Meta:
        db_table = 'status_voo'
         
class Rota(models.Model):
    id = models.IntegerField(primary_key=True)
    aeroporto_partida = models.CharField(max_length=200, null=False)
    aeroporto_chegada = models.CharField(max_length=200, null=False)
    
    class Meta:
        db_table = 'rotas'

class Voo(models.Model):
    id = models.IntegerField(primary_key=True)
    rota = models.ForeignKey(Rota, on_delete=models.CASCADE, null=False)
    chegada_prevista = models.DateTimeField(null=False)
    partida_prevista = models.DateTimeField(null=False)
    companhia_aerea = models.CharField(max_length=200, null=False)
    class Meta:
        db_table = 'voos'

class VooDinamico(models.Model):
    id = models.IntegerField(primary_key=True)
    voo = models.ForeignKey(Voo, on_delete=models.CASCADE, null=False)
    status = models.ForeignKey(StatusVoo, on_delete=models.CASCADE, null=False)
    partida_real = models.DateTimeField()
    chegada_real = models.DateTimeField()
    class Meta:
        db_table = 'voo_dinamico' 
        
class Conexao(models.Model):
    id = models.IntegerField(primary_key=True)
    rota = models.ForeignKey(Rota, on_delete=models.CASCADE, null=False)
    num_conexao = models.IntegerField(null=False)
    titulo = models.CharField(max_length=200,null=False)
    class Meta:
        db_table = 'conexoes'  