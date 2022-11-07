from django.test import TestCase
import datetime
from flight.models import *
from .forms import *
from .views import is_new_status_valid

class StatusVooTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        StatusVoo.objects.create(id=1, titulo='Em rota')
    
    def test_create_read_id(self):
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
    
    def test_create_read_conexao(self):
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

    def test_create_read_voo(self):
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

    def test_create_read_voo_dinamico(self):
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

class CrudFormValidationTest(TestCase):
    def test_incomplete_create_voo_form(self):
        voo_data = {
            "companhia_aerea": "GOL", 
            "previsao_de_partida": datetime.datetime(2022, 10, 15, 21, 13), 
            "previsao_de_chegada": datetime.datetime(2022, 10, 15, 22, 13), 
            "rota": ""
        }

        form = CreateVoo(voo_data)
        self.assertFalse(form.is_valid())

    def test_incomplete_update_voo_form(self):
        rota = Rota.objects.create(id=123, 
                                   aeroporto_partida="Aeroporto 1", 
                                   aeroporto_chegada="Aeroporto 2")
        voo_data = {
            "companhia_aerea": "", 
            "previsao_de_partida": datetime.datetime(2022, 10, 15, 21, 13), 
            "previsao_de_chegada": datetime.datetime(2022, 10, 15, 22, 13), 
            "rota": rota
        }

        form = UpdateVoo(voo_data)
        self.assertFalse(form.is_valid())

    def test_type_error_form(self):
        rota = Rota.objects.create(id=123, 
                                   aeroporto_partida="Aeroporto 1", 
                                   aeroporto_chegada="Aeroporto 2")
        voo_data = {
            "companhia_aerea": "GOL", 
            "previsao_de_partida": "input_invalido", 
            "previsao_de_chegada": datetime.datetime(2022, 10, 15, 22, 13), 
            "rota": rota
        }

        form = UpdateVoo(voo_data)
        self.assertFalse(form.is_valid())

    def test_valid_create_form(self):
        rota = Rota.objects.create(id=123, 
                                   aeroporto_partida="Aeroporto 1", 
                                   aeroporto_chegada="Aeroporto 2")
        voo_data = {
            "companhia_aerea": "GOL", 
            "previsao_de_partida": datetime.datetime(2022, 10, 15, 21, 13), 
            "previsao_de_chegada": datetime.datetime(2022, 10, 15, 22, 13), 
            "rota": rota
        }

        form = CreateVoo(voo_data)
        self.assertTrue(form.is_valid())

class UpdateFlightStatusTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        StatusVoo.objects.create(titulo="Embarcando")
        StatusVoo.objects.create(titulo="Cancelado")
        StatusVoo.objects.create(titulo="Programado")
        StatusVoo.objects.create(titulo="Taxiando")
        StatusVoo.objects.create(titulo="Pronto")
        StatusVoo.objects.create(titulo="Autorizado")
        StatusVoo.objects.create(titulo="Em voo")
        StatusVoo.objects.create(titulo="Aterrissando")
        StatusVoo.objects.create(titulo="-")

    def test_ok_1(self):
        current_status = StatusVoo.objects.get(titulo="-")
        new_status = StatusVoo.objects.get(titulo="Embarcando")
        self.assertTrue(is_new_status_valid(current_status.id, new_status.id))

        current_status = StatusVoo.objects.get(titulo="-")
        new_status = StatusVoo.objects.get(titulo="Cancelado")
        self.assertTrue(is_new_status_valid(current_status.id, new_status.id))

    def test_ok_2(self):
        current_status = StatusVoo.objects.get(titulo="Embarcando")
        new_status = StatusVoo.objects.get(titulo="Programado")
        self.assertTrue(is_new_status_valid(current_status.id, new_status.id))

        current_status = StatusVoo.objects.get(titulo="Programado")
        new_status = StatusVoo.objects.get(titulo="Taxiando")
        self.assertTrue(is_new_status_valid(current_status.id, new_status.id))

        current_status = StatusVoo.objects.get(titulo="Taxiando")
        new_status = StatusVoo.objects.get(titulo="Pronto")
        self.assertTrue(is_new_status_valid(current_status.id, new_status.id))

        current_status = StatusVoo.objects.get(titulo="Pronto")
        new_status = StatusVoo.objects.get(titulo="Autorizado")
        self.assertTrue(is_new_status_valid(current_status.id, new_status.id))

        current_status = StatusVoo.objects.get(titulo="Autorizado")
        new_status = StatusVoo.objects.get(titulo="Em voo")
        self.assertTrue(is_new_status_valid(current_status.id, new_status.id))

        current_status = StatusVoo.objects.get(titulo="Em voo")
        new_status = StatusVoo.objects.get(titulo="Aterrissando")
        self.assertTrue(is_new_status_valid(current_status.id, new_status.id))

    def test_invalid_1(self):
        # Não é possível transitar para outro status, uma vez que o voo está cancelado
        current_status = StatusVoo.objects.get(titulo="Cancelado")

        new_status = StatusVoo.objects.get(titulo="Embarcando")
        self.assertFalse(is_new_status_valid(current_status.id, new_status.id))

        new_status = StatusVoo.objects.get(titulo="Programado")
        self.assertFalse(is_new_status_valid(current_status.id, new_status.id))

        new_status = StatusVoo.objects.get(titulo="Taxiando")
        self.assertFalse(is_new_status_valid(current_status.id, new_status.id))

        new_status = StatusVoo.objects.get(titulo="Pronto")
        self.assertFalse(is_new_status_valid(current_status.id, new_status.id))

        new_status = StatusVoo.objects.get(titulo="Autorizado")
        self.assertFalse(is_new_status_valid(current_status.id, new_status.id))

        new_status = StatusVoo.objects.get(titulo="Em voo")
        self.assertFalse(is_new_status_valid(current_status.id, new_status.id))

        new_status = StatusVoo.objects.get(titulo="Aterrissando")
        self.assertFalse(is_new_status_valid(current_status.id, new_status.id))

    def test_invalid_2(self):
        # Casos de transições inválidas que não seguem a ordem lógica da transição dos status
        current_status = StatusVoo.objects.get(titulo="Embarcando")
        new_status = StatusVoo.objects.get(titulo="Taxiando")
        self.assertFalse(is_new_status_valid(current_status.id, new_status.id))

        current_status = StatusVoo.objects.get(titulo="Programado")
        new_status = StatusVoo.objects.get(titulo="Em voo")
        self.assertFalse(is_new_status_valid(current_status.id, new_status.id))

        current_status = StatusVoo.objects.get(titulo="Taxiando")
        new_status = StatusVoo.objects.get(titulo="Programado")
        self.assertFalse(is_new_status_valid(current_status.id, new_status.id))

        current_status = StatusVoo.objects.get(titulo="Pronto")
        new_status = StatusVoo.objects.get(titulo="Embarcando")
        self.assertFalse(is_new_status_valid(current_status.id, new_status.id))

        current_status = StatusVoo.objects.get(titulo="Autorizado")
        new_status = StatusVoo.objects.get(titulo="Aterrissando")
        self.assertFalse(is_new_status_valid(current_status.id, new_status.id))

        current_status = StatusVoo.objects.get(titulo="Em voo")
        new_status = StatusVoo.objects.get(titulo="Cancelado")
        self.assertFalse(is_new_status_valid(current_status.id, new_status.id))

class ReportFormTest(TestCase):

    def test_initial_date_after_final_date(self):
        """Test form is invalid if initial_date is after final_date."""
        initial_date = datetime.datetime.strptime('02/10/21', '%d/%m/%y').date()
        final_date = datetime.datetime.strptime('01/10/21', '%d/%m/%y').date()
        form = ReportForm(data={'report_type': '1','initial_date': initial_date, 'final_date': final_date})
        self.assertFalse(form.is_valid())

    def test_initial_date_after_current_date(self):
        """Test form is invalid if initial_date is after current date."""
        initial_date = datetime.date.today() + datetime.timedelta(days=1)
        final_date = datetime.date.today() - datetime.timedelta(days=1)
        form = ReportForm(data={'report_type': '1','initial_date': initial_date, 'final_date': final_date})
        self.assertFalse(form.is_valid())

    def test_final_date_after_current_date(self):
        """Test form is invalid if final_date is after current date."""
        initial_date = datetime.date.today() - datetime.timedelta(days=1)
        final_date = datetime.date.today() + datetime.timedelta(days=1)
        form = ReportForm(data={'report_type': '1','initial_date': initial_date, 'final_date': final_date})
        self.assertFalse(form.is_valid())

    def test_working_inputs(self):
        """Test form is valid."""
        initial_date = datetime.date.today() - datetime.timedelta(days=2)
        final_date = datetime.date.today() - datetime.timedelta(days=1)
        form = ReportForm(data={'report_type': '1','initial_date': initial_date, 'final_date': final_date})
        self.assertTrue(form.is_valid())
