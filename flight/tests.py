from django.test import TestCase
import datetime
from flight.models import *

class StatusVooTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        StatusVoo.objects.create(id=1, titulo='Em rota')
    
    def test_create_id(self):
        status_1 = StatusVoo.objects.get(id=1)
        self.assertEqual(status_1.id, 1)
        self.assertEqual(status_1.titulo, 'Em rota')

    def test_update_voo_dinamico(self):
        status_1 =StatusVoo.objects.get(id=1)
        StatusVoo.objects.filter(id=1).update(titulo='Programado')
        status_2 = StatusVoo.objects.get(id=1)
        self.assertEqual(status_2.id, 1)
        self.assertEqual(status_2.titulo, 'Programado')
    
    def test_delete_voo_dinamico(self):
        tamOrig = len(StatusVoo.objects.all())
        StatusVoo.objects.filter(id=1).delete()
        tamFinal = len(StatusVoo.objects.all())
        self.assertEqual(tamFinal, tamOrig - 1)

class RotaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Rota.objects.create(id=1,
                            aeroporto_partida='Sao Paulo',
                            aeroporto_chegada='Londres')

    def test_create_read_rota(self):
        rota_1 = Rota.objects.get(id=1)
        self.assertEqual(rota_1.id, 1)
        self.assertEqual(rota_1.aeroporto_partida, 'Sao Paulo')
        self.assertEqual(rota_1.aeroporto_chegada, 'Londres')

    def test_update_rota(self):
        Rota.objects.filter(id=1).update(aeroporto_partida='Rio de Janeiro',
                                         aeroporto_chegada='Acre')   
        rota_atualizada = Rota.objects.get(id=1)
        self.assertEqual(rota_atualizada.id, 1)
        self.assertEqual(rota_atualizada.aeroporto_partida, 'Rio de Janeiro')
        self.assertEqual(rota_atualizada.aeroporto_chegada, 'Acre')

    def test_delete_rota(self):
        tamOrig = len(Rota.objects.all())
        Rota.objects.filter(id=1).delete()
        tamFinal = len(Rota.objects.all())
        self.assertEqual(tamFinal, tamOrig - 1)     

class ConexaoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        rota = Rota.objects.create(id=345,
                                   aeroporto_partida="Aeroporto 1", 
                                   aeroporto_chegada="Aeroporto 2")
        Conexao.objects.create(id=1,
                               rota=rota,
                               num_conexao=321,
                               titulo='GRU')
    
    def test_create_conexao(self):
        conexao_1 = Conexao.objects.get(id=1)
        self.assertEqual(conexao_1.id, 1)
        self.assertEqual(conexao_1.num_conexao, 321)
        self.assertEqual(conexao_1.titulo, 'GRU')
       
    def test_update_conexao(self):
        Conexao.objects.filter(id = 1).update(num_conexao=123,
                                              titulo='CONG')
        conexao_atualizada = Conexao.objects.get(id = 1)
        self.assertEqual(conexao_atualizada.id, 1)
        self.assertEqual(conexao_atualizada.num_conexao, 123)
        self.assertEqual(conexao_atualizada.titulo, 'CONG')
    
    def test_delete_conexao(self):
        tamOrig = len(Conexao.objects.all())
        Conexao.objects.filter(id=1).delete()
        tamFinal = len(Conexao.objects.all())
        self.assertEqual(tamFinal, tamOrig - 1)  
        
class VooTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        rota = Rota.objects.create(id=123, 
                                   aeroporto_partida="Aeroporto 1", 
                                   aeroporto_chegada="Aeroporto 2")
        Voo.objects.create(id=1234,
                           rota=rota,
                           chegada_prevista=datetime.datetime(2022, 6, 10, 16, 00),
                           partida_prevista=datetime.datetime(2022, 6, 10, 10, 00),
                           companhia_aerea="Companhia 1")

    def test_create_voo(self):
        voo_teste = Voo.objects.get(id=1234)
        self.assertEqual(voo_teste.id, 1234)
        self.assertEqual(voo_teste.chegada_prevista.strftime("%Y-%m-%d %H:%M:%S"), "2022-06-10 16:00:00")
        self.assertEqual(voo_teste.partida_prevista.strftime("%Y-%m-%d %H:%M:%S"), "2022-06-10 10:00:00")
        self.assertEqual(voo_teste.companhia_aerea, "Companhia 1")
        self.assertEqual(voo_teste.rota.id, 123)
        self.assertEqual(voo_teste.rota.aeroporto_partida, "Aeroporto 1")
        self.assertEqual(voo_teste.rota.aeroporto_chegada, "Aeroporto 2")

    def test_update_voo(self):
        voo_teste = Voo.objects.get(id=1234)
        Voo.objects.filter(id=voo_teste.id).update(partida_prevista=datetime.datetime(2022, 10, 10, 16, 00), 
                                                   chegada_prevista=datetime.datetime(2022, 10, 10, 10, 00),
                                                   companhia_aerea="Companhia 2")
        voo_teste = Voo.objects.get(id=1234)
        self.assertEqual(voo_teste.id, 1234)
        self.assertNotEqual(voo_teste.companhia_aerea, "Companhia 1")
        self.assertEqual(voo_teste.companhia_aerea, "Companhia 2")
        self.assertEqual(voo_teste.partida_prevista.strftime("%Y-%m-%d %H:%M:%S"), "2022-10-10 16:00:00")
        self.assertEqual(voo_teste.chegada_prevista.strftime("%Y-%m-%d %H:%M:%S"), "2022-10-10 10:00:00")

    def test_delete_voo(self):
        tamOrig = len(Voo.objects.all())
        Voo.objects.filter(id=1234).delete()
        tamFinal = len(VooDinamico.objects.all())
        self.assertEqual(tamFinal, tamOrig - 1)

class VooDinamicoTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        status = StatusVoo.objects.create(id=1, titulo='Em rota')
        rota = Rota.objects.create(id=123, 
                                   aeroporto_partida="Aeroporto 1", 
                                   aeroporto_chegada="Aeroporto 2")
        voo = Voo.objects.create(id=1,
                                 rota=rota,
                                 partida_prevista=datetime.datetime(2022, 8, 15, 22, 15), 
                                 chegada_prevista=datetime.datetime(2022, 8, 16,  9, 30), 
                                 companhia_aerea="Ponei aerlines")
        VooDinamico.objects.create(id=1, 
                                   voo=voo, 
                                   status=status,
                                   partida_real=datetime.datetime(2022, 8, 15, 21, 13), 
                                   chegada_real=datetime.datetime(2022, 8, 16,  9, 43))

    def test_create_voo_dinamico(self):
        voo_din_1 = VooDinamico.objects.get(id=1)
        self.assertEqual(voo_din_1.id, 1)
        self.assertEqual(voo_din_1.voo.id, 1)
        self.assertEqual(voo_din_1.status.titulo, "Em rota")
        self.assertEqual(voo_din_1.partida_real.strftime("%Y-%m-%d %H:%M:%S"), "2022-08-15 21:13:00")
        self.assertEqual(voo_din_1.chegada_real.strftime("%Y-%m-%d %H:%M:%S"), "2022-08-16 09:43:00")

    def test_update_voo_dinamico(self):
        voo_din_1 = VooDinamico.objects.get(id=1)
        VooDinamico.objects.filter(id=voo_din_1.id).update(partida_real=datetime.datetime(2022, 10, 15, 21, 13), 
                                                           chegada_real=datetime.datetime(2022, 10, 16,  9, 43))
        voo_din_2 = VooDinamico.objects.get(id=1)
        self.assertEqual(voo_din_2.id, 1)
        self.assertEqual(voo_din_2.voo.id, 1)
        self.assertEqual(voo_din_2.status.titulo, "Em rota")
        self.assertEqual(voo_din_2.partida_real.strftime("%Y-%m-%d %H:%M:%S"), "2022-10-15 21:13:00")
        self.assertEqual(voo_din_2.chegada_real.strftime("%Y-%m-%d %H:%M:%S"), "2022-10-16 09:43:00")
    
    def test_delete_voo_dinamico(self):
        tamOrig = len(VooDinamico.objects.all())
        VooDinamico.objects.filter(id=1).delete()
        tamFinal = len(VooDinamico.objects.all())
        self.assertEqual(tamFinal, tamOrig - 1)
