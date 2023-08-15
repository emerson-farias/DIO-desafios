import unittest
from unittest.mock import patch
from io import StringIO
from banking_system import *

class BankingSystemUnitTest(unittest.TestCase):
    ###################
    # Tests for deposit
    ###################

    def test_deposit_positive_amount(self):
        amount = 100.0
        balance = 500.0
        new_balance, statement_line = deposit(amount, balance)
        self.assertEqual(new_balance, 600.0)
        self.assertIn("Deposit", statement_line)
        self.assertIn(str(amount), statement_line)

    def test_deposit_zero_amount(self):
        amount = 0.0
        balance = 500.0
        new_balance, statement_line = deposit(amount, balance)
        self.assertEqual(new_balance, 500.0)
        self.assertEqual(statement_line, "")

    def test_deposit_negative_amount(self):
        amount = -100.0
        balance = 500.0
        new_balance, statement_line = deposit(amount, balance)
        self.assertEqual(new_balance, 500.0)
        self.assertEqual(statement_line, "")

    #####################################
    # Tests for exceeded_withdrawal_count
    #####################################

    def test_exceeded_withdrawal_count_within_limit(self):
        number_of_withdrawals = WITHDRAWAL_LIMIT_COUNT - 1
        result = exceeded_withdrawal_count(number_of_withdrawals)
        self.assertFalse(result)

    def test_exceeded_withdrawal_count_at_limit(self):
        number_of_withdrawals = WITHDRAWAL_LIMIT_COUNT
        result = exceeded_withdrawal_count(number_of_withdrawals)
        self.assertTrue(result)

    def test_exceeded_withdrawal_count_above_limit(self):
        number_of_withdrawals = WITHDRAWAL_LIMIT_COUNT + 1
        result = exceeded_withdrawal_count(number_of_withdrawals)
        self.assertTrue(result)

    ####################
    # Tests for withdraw
    ####################

    def test_withdraw_positive_amount(self):
        amount = 100.0
        balance = 500.0
        withdrawal_count = 0
        new_balance, new_withdrawal_count, statement_line = withdraw(amount=amount, balance=balance, number_of_withdrawals=withdrawal_count)
        self.assertEqual(new_balance, 400.0)
        self.assertEqual(new_withdrawal_count, 1)
        self.assertIn("Withdraw", statement_line)
        self.assertIn(str(amount), statement_line)

    def test_withdraw_zero_amount(self):
        amount = 0.0
        balance = 500.0
        withdrawal_count = 0
        new_balance, new_withdrawal_count, statement_line = withdraw(amount=amount, balance=balance, number_of_withdrawals=withdrawal_count)
        self.assertEqual(new_balance, 500.0)
        self.assertEqual(new_withdrawal_count, 0)
        self.assertEqual(statement_line, "")

    def test_withdraw_negative_amount(self):
        amount = -100.0
        balance = 500.0
        withdrawal_count = 0
        new_balance, new_withdrawal_count, statement_line = withdraw(amount=amount, balance=balance, number_of_withdrawals=withdrawal_count)
        self.assertEqual(new_balance, 500.0)
        self.assertEqual(new_withdrawal_count, 0)
        self.assertEqual(statement_line, "")

    def test_withdraw_amount_over_limit(self):
        amount = WITHDRAWAL_LIMIT_AMOUNT + 50.0
        balance = 1000.0
        withdrawal_count = 0
        new_balance, new_withdrawal_count, statement_line = withdraw(amount=amount, balance=balance, number_of_withdrawals=withdrawal_count)
        self.assertEqual(new_balance, 1000.0)
        self.assertEqual(new_withdrawal_count, 0)
        self.assertEqual(statement_line, "")

    def test_withdraw_insufficient_balance(self):
        amount = 600.0
        balance = 500.0
        withdrawal_count = 0
        new_balance, new_withdrawal_count, statement_line = withdraw(amount=amount, balance=balance, number_of_withdrawals=withdrawal_count)
        self.assertEqual(new_balance, 500.0)
        self.assertEqual(new_withdrawal_count, 0)
        self.assertEqual(statement_line, "")

class BankingSystemIntegrationTest(unittest.TestCase):
    @patch('builtins.input', side_effect=['d', '200', 's', 'q'])
    @patch('sys.stdout', new_callable=StringIO)
    def test01_deposit(self, mock_output, mock_input):
        main()
        self.assertIn("Deposit     -     200.00 USD", mock_output.getvalue())
        self.assertIn("Net Balance -     200.00 USD", mock_output.getvalue())

    @patch('builtins.input', side_effect=['d', '200', 'w', '200', 's', 'q'])
    @patch('sys.stdout', new_callable=StringIO)
    def test02_withdraw(self, mock_output, mock_input):
        main()
        self.assertIn("Deposit     -     200.00 USD", mock_output.getvalue())
        self.assertIn("Withdraw    -    -200.00 USD", mock_output.getvalue())
        self.assertIn("Net Balance -       0.00 USD", mock_output.getvalue())

    @patch('builtins.input', side_effect=['d', '600', 'w', f'{WITHDRAWAL_LIMIT_AMOUNT + 50.0}', 'w', '100', 'w', '200', 'w', '305', 'w', '295', 'w', 's', 'q'])
    @patch('sys.stdout', new_callable=StringIO)
    def test03_withdraws(self, mock_output, mock_input):
        main()
        self.assertIn("Deposit     -     600.00 USD", mock_output.getvalue())
        self.assertIn("ERROR: Amount exceeds allowed withdrawal limit", mock_output.getvalue())
        self.assertIn("Withdraw    -    -100.00 USD", mock_output.getvalue())
        self.assertIn("Withdraw    -    -200.00 USD", mock_output.getvalue())
        self.assertIn("ERROR: Insufficient balance", mock_output.getvalue())
        self.assertIn("Withdraw    -    -295.00 USD", mock_output.getvalue())
        self.assertIn("ERROR: Daily withdrawal limit exceeded", mock_output.getvalue())
        self.assertIn("Net Balance -       5.00 USD", mock_output.getvalue())

if __name__ == '__main__':
    unittest.main()
