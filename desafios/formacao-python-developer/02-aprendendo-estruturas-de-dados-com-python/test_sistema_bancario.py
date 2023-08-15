import unittest
from unittest.mock import patch
from io import StringIO
from sistema_bancario import *

class UnitTestSistemaBancario(unittest.TestCase):
    #######################
    # Testes para depositar
    #######################

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

    #######################################
    # Testes para excedeu_quantidade_saques
    #######################################

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

    ###################
    # Testes para sacar
    ###################

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
    @patch('builtins.input', side_effect=['d', '200', 'e', 'q'])
    @patch('sys.stdout', new_callable=StringIO)
    def test01_depositar(self, mock_output, mock_input):
        main()
        self.assertIn("Depósito - R$     200.00 C", mock_output.getvalue())
        self.assertIn("Saldo    - R$     200.00", mock_output.getvalue())

    @patch('builtins.input', side_effect=['d', '200', 's', '200', 'e', 'q'])
    @patch('sys.stdout', new_callable=StringIO)
    def test02_saque(self, mock_output, mock_input):
        main()
        self.assertIn("Saque    - R$     200.00 D", mock_output.getvalue())
        self.assertIn("Saldo    - R$       0.00", mock_output.getvalue())

    @patch('builtins.input', side_effect=['d', '600', 's', f'{LIMITE_VALOR_SAQUE + 50.0}', 's', '100', 's', '200', 's', '305', 's', '295', 's', 'e', 'q'])
    @patch('sys.stdout', new_callable=StringIO)
    def test03_saques(self, mock_output, mock_input):
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