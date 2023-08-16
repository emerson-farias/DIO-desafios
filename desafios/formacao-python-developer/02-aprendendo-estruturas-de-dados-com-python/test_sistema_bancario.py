import unittest
from unittest.mock import patch
from io import StringIO
from sistema_bancario import *

class UnitTestSistemaBancario(unittest.TestCase):

# ##############################################################################
# ▒█░▒█ █▀▀ █░░█ █▀▀█ █▀▀█ ░▀░ █▀▀█ █▀▀ 
# ▒█░▒█ ▀▀█ █░░█ █▄▄█ █▄▄▀ ▀█▀ █░░█ ▀▀█ 
# ░▀▄▄▀ ▀▀▀ ░▀▀▀ ▀░░▀ ▀░▀▀ ▀▀▀ ▀▀▀▀ ▀▀▀ 
# ##############################################################################

    def test_buscar_usuario(self):
        usuarios = [
            {'cpf': '12345678901', 'nome': 'João'},
            {'cpf': '98765432109', 'nome': 'Maria'}
        ]
        usuario = buscar_usuario(usuarios, cpf='12345678901')
        self.assertEqual(usuario, {'cpf': '12345678901', 'nome': 'João'})
        usuario = buscar_usuario(usuarios, cpf='00000000000')
        self.assertIsNone(usuario)

    def test_criar_usuario_com_sucesso(self):
        usuarios = []
        usuario = criar_usuario(usuarios, cpf="12345678901", nome="João", data_nascimento="01/11/2000", endereco="Rua das Flores, 123 - Jardim Primavera - São Paulo/SP")
        self.assertEqual(usuario['cpf'], "12345678901")
        self.assertEqual(usuario['nome'], "João")
        self.assertEqual(usuario['data_nascimento'], "01/11/2000")
        self.assertEqual(usuario['endereco'], "Rua das Flores, 123 - Jardim Primavera - São Paulo/SP")

    def test_criar_usuario_com_cpf_duplicado(self):
        usuarios = []
        usuario = criar_usuario(usuarios, cpf="12345678901", nome="João", data_nascimento="01/11/2000", endereco="Rua das Flores, 123 - Jardim Primavera - São Paulo/SP")
        with self.assertRaises(ValueError) as context:
            criar_usuario(usuarios, cpf="12345678901", nome="Maria", data_nascimento="02/12/2001", endereco="Rua das Flores, 456 - Jardim Primavera - São Paulo/SP")
        self.assertEqual(str(context.exception), ERRO_JA_EXISTE_USUARIO)

# ##############################################################################
# ▒█▀▀█ █▀▀█ █▀▀▄ ▀▀█▀▀ █▀▀█ ░░ ▒█▀▀█ █▀▀█ █▀▀█ █▀▀█ █▀▀ █▀▀▄ ▀▀█▀▀ █▀▀ 
# ▒█░░░ █░░█ █░░█ ░░█░░ █▄▄█ ▀▀ ▒█░░░ █░░█ █▄▄▀ █▄▄▀ █▀▀ █░░█ ░░█░░ █▀▀ 
# ▒█▄▄█ ▀▀▀▀ ▀░░▀ ░░▀░░ ▀░░▀ ░░ ▒█▄▄█ ▀▀▀▀ ▀░▀▀ ▀░▀▀ ▀▀▀ ▀░░▀ ░░▀░░ ▀▀▀
# ##############################################################################

    # ##########################################################################
    # Testes para depositar
    # ##########################################################################

    def test_depositar_valor_positivo(self):
        valor = 100.0
        saldo = 500.0
        novo_saldo, linha_extrato = depositar(valor, saldo)
        self.assertEqual(novo_saldo, 600.0)
        self.assertIn("Depósito", linha_extrato)
        self.assertIn(str(valor), linha_extrato)

    def test_depositar_valor_zero(self):
        valor = 0.0
        saldo = 500.0
        novo_saldo, linha_extrato = depositar(valor, saldo)
        self.assertEqual(novo_saldo, 500.0)
        self.assertEqual(linha_extrato, "")

    def test_depositar_valor_negativo(self):
        valor = -100.0
        saldo = 500.0
        novo_saldo, linha_extrato = depositar(valor, saldo)
        self.assertEqual(novo_saldo, 500.0)
        self.assertEqual(linha_extrato, "")

    # ##########################################################################
    # Testes para excedeu_quantidade_saques
    # ##########################################################################

    def test_excedeu_quantidade_saques_dentro_limite(self):
        numero_saques = LIMITE_QUANTIDADE_SAQUES - 1
        resultado = excedeu_quantidade_saques(numero_saques)
        self.assertFalse(resultado)

    def test_excedeu_quantidade_saques_no_limite(self):
        numero_saques = LIMITE_QUANTIDADE_SAQUES
        resultado = excedeu_quantidade_saques(numero_saques)
        self.assertTrue(resultado)

    def test_excedeu_quantidade_saques_acima_limite(self):
        numero_saques = LIMITE_QUANTIDADE_SAQUES + 1
        resultado = excedeu_quantidade_saques(numero_saques)
        self.assertTrue(resultado)

    # ##########################################################################
    # Testes para sacar
    # ##########################################################################

    def test_sacar_valor_positivo(self):
        valor = 100.0
        saldo = 500.0
        numero_saques = 0
        novo_saldo, novo_numero_saques, linha_extrato = sacar(valor=valor, saldo=saldo, numero_saques=numero_saques)
        self.assertEqual(novo_saldo, 400.0)
        self.assertEqual(novo_numero_saques, 1)
        self.assertIn("Saque", linha_extrato)
        self.assertIn(str(valor), linha_extrato)

    def test_sacar_valor_zero(self):
        valor = 0.0
        saldo = 500.0
        numero_saques = 0
        novo_saldo, novo_numero_saques, linha_extrato = sacar(valor=valor, saldo=saldo, numero_saques=numero_saques)
        self.assertEqual(novo_saldo, 500.0)
        self.assertEqual(novo_numero_saques, 0)
        self.assertEqual(linha_extrato, "")

    def test_sacar_valor_negativo(self):
        valor = -100.0
        saldo = 500.0
        numero_saques = 0
        novo_saldo, novo_numero_saques, linha_extrato = sacar(valor=valor, saldo=saldo, numero_saques=numero_saques)
        self.assertEqual(novo_saldo, 500.0)
        self.assertEqual(novo_numero_saques, 0)
        self.assertEqual(linha_extrato, "")

    def test_sacar_valor_acima_limite(self):
        valor = LIMITE_VALOR_SAQUE + 50.0
        saldo = 1000.0
        numero_saques = 0
        novo_saldo, novo_numero_saques, linha_extrato = sacar(valor=valor, saldo=saldo, numero_saques=numero_saques)
        self.assertEqual(novo_saldo, 1000.0)
        self.assertEqual(novo_numero_saques, 0)
        self.assertEqual(linha_extrato, "")

    def test_sacar_sem_saldo(self):
        valor = 600.0
        saldo = 500.0
        numero_saques = 0
        novo_saldo, novo_numero_saques, linha_extrato = sacar(valor=valor, saldo=saldo, numero_saques=numero_saques)
        self.assertEqual(novo_saldo, 500.0)
        self.assertEqual(novo_numero_saques, 0)
        self.assertEqual(linha_extrato, "")

class IntegrationTestSistemaBancario(unittest.TestCase):

# ##############################################################################
# ▒█░▒█ █▀▀ █░░█ █▀▀█ █▀▀█ ░▀░ █▀▀█ █▀▀ 
# ▒█░▒█ ▀▀█ █░░█ █▄▄█ █▄▄▀ ▀█▀ █░░█ ▀▀█ 
# ░▀▄▄▀ ▀▀▀ ░▀▀▀ ▀░░▀ ▀░▀▀ ▀▀▀ ▀▀▀▀ ▀▀▀ 
# ##############################################################################

    @patch('builtins.input', side_effect=['u', 'c', '12345678901', 'João', '01/01/2000', 'Rua A, 123', 'q', 'q'])
    @patch('sys.stdout', new_callable=StringIO)
    def test01_administrar_usuarios_criar_usuario(self, mock_output, mock_input):
        main()
        self.assertIn(MSG_USUARIO_CRIADO, mock_output.getvalue())

    @patch('builtins.input', side_effect=['u', 'c', '12345678901', 'João', '01/01/2000', 'Rua A, 123', 'l', 'q', 'q'])
    @patch('sys.stdout', new_callable=StringIO)
    def test02_administrar_usuarios_listar_usuarios(self, mock_output, mock_input):
        main()
        self.assertIn("12345678901", mock_output.getvalue())
        self.assertIn("João", mock_output.getvalue())
        self.assertIn("01/01/2000", mock_output.getvalue())
        self.assertIn("Rua A, 123", mock_output.getvalue())    

    @patch('builtins.input', side_effect=['u', 'c', '12345678901', 'João', '01/01/2000', 'Rua A, 123', 'c', '12345678901', 'Jane Smith', '02/02/2002', '456 Elm St', 'q', 'q'])
    @patch('sys.stdout', new_callable=StringIO)
    def test03_administrar_usuarios_criar_usuario_existente(self, mock_output, mock_input):
        main()
        self.assertIn(ERRO_JA_EXISTE_USUARIO, mock_output.getvalue())

# ##############################################################################
# ▒█▀▀█ █▀▀█ █▀▀▄ ▀▀█▀▀ █▀▀█ ░░ ▒█▀▀█ █▀▀█ █▀▀█ █▀▀█ █▀▀ █▀▀▄ ▀▀█▀▀ █▀▀ 
# ▒█░░░ █░░█ █░░█ ░░█░░ █▄▄█ ▀▀ ▒█░░░ █░░█ █▄▄▀ █▄▄▀ █▀▀ █░░█ ░░█░░ █▀▀ 
# ▒█▄▄█ ▀▀▀▀ ▀░░▀ ░░▀░░ ▀░░▀ ░░ ▒█▄▄█ ▀▀▀▀ ▀░▀▀ ▀░▀▀ ▀▀▀ ▀░░▀ ░░▀░░ ▀▀▀
# ##############################################################################

    @patch('builtins.input', side_effect=['a', 'd', '200', 'e', 'q', 'q'])
    @patch('sys.stdout', new_callable=StringIO)
    def test04_depositar(self, mock_output, mock_input):
        main()
        self.assertIn("Depósito - R$     200.00 C", mock_output.getvalue())
        self.assertIn("Saldo    - R$     200.00", mock_output.getvalue())

    @patch('builtins.input', side_effect=['a', 'd', '200', 's', '200', 'e', 'q', 'q'])
    @patch('sys.stdout', new_callable=StringIO)
    def test05_saque(self, mock_output, mock_input):
        main()
        self.assertIn("Saque    - R$     200.00 D", mock_output.getvalue())
        self.assertIn("Saldo    - R$       0.00", mock_output.getvalue())

    @patch('builtins.input', side_effect=['a', 'd', '600', 's', f'{LIMITE_VALOR_SAQUE + 50.0}', 's', '100', 's', '200', 's', '305', 's', '295', 's', 'e', 'q', 'q'])
    @patch('sys.stdout', new_callable=StringIO)
    def test06_saques(self, mock_output, mock_input):
        main()
        self.assertIn("Depósito - R$     600.00 C", mock_output.getvalue())
        self.assertIn("ERRO: Valor maior que limite de saque permitido", mock_output.getvalue())
        self.assertIn("Saque    - R$     100.00 D", mock_output.getvalue())
        self.assertIn("Saque    - R$     200.00 D", mock_output.getvalue())
        self.assertIn("ERRO: Saldo insuficiente", mock_output.getvalue())
        self.assertIn("Saque    - R$     295.00 D", mock_output.getvalue())
        self.assertIn("ERRO: Quantidade limite de saques diários excedido", mock_output.getvalue())
        self.assertIn("Saldo    - R$       5.00", mock_output.getvalue())

if __name__ == '__main__':
    unittest.main()