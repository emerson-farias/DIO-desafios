import unittest
from unittest.mock import patch
from io import StringIO
from banking_system import *

class BankingSystemUnitTest(unittest.TestCase):

# ##############################################################################
# ▒█░▒█ █▀▀ █▀▀ █▀▀█ █▀▀ 
# ▒█░▒█ ▀▀█ █▀▀ █▄▄▀ ▀▀█ 
# ░▀▄▄▀ ▀▀▀ ▀▀▀ ▀░▀▀ ▀▀▀
# ##############################################################################

    def test_search_user(self):
        users = [
            {'ssn': '123456789', 'name': 'John'},
            {'ssn': '987654321', 'name': 'Jane'}
        ]
        user = search_user(users, ssn='123456789')
        self.assertEqual(user, {'ssn': '123456789', 'name': 'John'})
        user = search_user(users, ssn='000.000.000-00')
        self.assertIsNone(user)

    def test_create_user_successfully(self):
        users = []
        user = create_user(users, ssn="123456789", name="John", birth_date="11/01/2000", address="Pine Street, 123 - Downtown - New York/NY")
        self.assertEqual(user['ssn'], "123456789")
        self.assertEqual(user['name'], "John")
        self.assertEqual(user['birth_date'], "11/01/2000")
        self.assertEqual(user['address'], "Pine Street, 123 - Downtown - New York/NY")

    def test_create_user_with_duplicate_ssn(self):
        users = []
        user = create_user(users, ssn="123456789", name="John", birth_date="11/01/2000", address="Pine Street, 123 - Downtown - New York/NY")
        with self.assertRaises(ValueError) as context:
            create_user(users, ssn="123456789", name="Jane", birth_date="12/02/2001", address="Pine Street, 456 - Downtown - New York/NY")
        self.assertEqual(str(context.exception), ERROR_USER_ALREADY_EXISTS)

# ##############################################################################
# ░█▀▀█ █▀▀ █▀▀ █▀▀█ █░░█ █▀▀▄ ▀▀█▀▀ █▀▀ 
# ▒█▄▄█ █░░ █░░ █░░█ █░░█ █░░█ ░░█░░ ▀▀█ 
# ▒█░▒█ ▀▀▀ ▀▀▀ ▀▀▀▀ ░▀▀▀ ▀░░▀ ░░▀░░ ▀▀▀
# ##############################################################################

    def test_list_accounts_empty(self):
        accounts = []
        with patch('sys.stdout', new_callable=StringIO) as mock_output:
            list_accounts(accounts)
            self.assertIn("No accounts.", mock_output.getvalue())

    def test_list_accounts_without_number(self):
        accounts = [
            {'branch': BRANCH, 'number': 1, 'holder': {'name': 'John', 'ssn': '123456789'}},
            {'branch': BRANCH, 'number': 2, 'holder': {'name': 'Jane', 'ssn': '987654321'}}
        ]
        with patch('sys.stdout', new_callable=StringIO) as mock_output:
            list_accounts(accounts)
            self.assertIn("Branch: " + BRANCH, mock_output.getvalue())
            self.assertIn("Account: 1", mock_output.getvalue())
            self.assertIn("Holder: John - 123456789", mock_output.getvalue())
            self.assertIn("Account: 2", mock_output.getvalue())
            self.assertIn("Holder: Jane - 987654321", mock_output.getvalue())

    def test_list_accounts_with_number(self):
        accounts = [
            {'branch': BRANCH, 'number': 1, 'holder': {'name': 'John', 'ssn': '123456789'}},
            {'branch': BRANCH, 'number': 2, 'holder': {'name': 'Jane', 'ssn': '987654321'}}
        ]
        with patch('sys.stdout', new_callable=StringIO) as mock_output:
            list_accounts(accounts, number=2)
            self.assertNotIn("Account: 1", mock_output.getvalue())
            self.assertIn("Account: 2", mock_output.getvalue())
            self.assertIn("Holder: Jane - 987654321", mock_output.getvalue())

    def test_create_account_with_existing_holder(self):
        users = [{'name': 'John', 'ssn': '123456789'}]
        accounts = []
        new_account = create_account(users, accounts, branch=BRANCH, holder_ssn='123456789')
        self.assertEqual(new_account['branch'], BRANCH)
        self.assertEqual(new_account['number'], 1)
        self.assertEqual(new_account['holder']['name'], 'John')
        self.assertEqual(new_account['holder']['ssn'], '123456789')

    def test_create_account_with_nonexistent_holder(self):
        users = [{'name': 'John', 'ssn': '123456789'}]
        accounts = []
        with self.assertRaises(ValueError) as context:
            create_account(users, accounts, branch=BRANCH, holder_ssn='987654321')
        self.assertEqual(str(context.exception), ERROR_USER_NOT_FOUND)

# ##############################################################################
# ▒█▀▀█ █░░█ █▀▀ █▀▀ █░█ ░▀░ █▀▀▄ █▀▀▀ 　 ░█▀▀█ █▀▀ █▀▀ █▀▀█ █░░█ █▀▀▄ ▀▀█▀▀ 
# ▒█░░░ █▀▀█ █▀▀ █░░ █▀▄ ▀█▀ █░░█ █░▀█ 　 ▒█▄▄█ █░░ █░░ █░░█ █░░█ █░░█ ░░█░░ 
# ▒█▄▄█ ▀░░▀ ▀▀▀ ▀▀▀ ▀░▀ ▀▀▀ ▀░░▀ ▀▀▀▀ 　 ▒█░▒█ ▀▀▀ ▀▀▀ ▀▀▀▀ ░▀▀▀ ▀░░▀ ░░▀░░
# ##############################################################################

    # ##########################################################################
    # Tests for deposit
    # ##########################################################################

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

    # ##########################################################################
    # Tests for exceeded_withdrawal_count
    # ##########################################################################

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

    # ##########################################################################
    # Tests for withdraw
    # ##########################################################################

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

# ##############################################################################
# ▒█░▒█ █▀▀ █▀▀ █▀▀█ █▀▀ 
# ▒█░▒█ ▀▀█ █▀▀ █▄▄▀ ▀▀█ 
# ░▀▄▄▀ ▀▀▀ ▀▀▀ ▀░▀▀ ▀▀▀
# ##############################################################################

    @patch('builtins.input', side_effect=['u', 'c', '123456789', 'John', '11/01/2000', '123 Pine St', 'q', 'q'])
    @patch('sys.stdout', new_callable=StringIO)
    def test01_manage_users_create_users(self, mock_output, mock_input):
        main()
        self.assertIn(MSG_USER_CREATED, mock_output.getvalue())

    @patch('builtins.input', side_effect=['u', 'c', '12345678901', 'John', '11/01/2000', '123 Pine St', 'l', 'q', 'q'])
    @patch('sys.stdout', new_callable=StringIO)
    def test02_manage_users_list_users(self, mock_output, mock_input):
        main()
        self.assertIn("12345678901", mock_output.getvalue())
        self.assertIn("John", mock_output.getvalue())
        self.assertIn("11/01/2000", mock_output.getvalue())
        self.assertIn("123 Pine St", mock_output.getvalue())    

    @patch('builtins.input', side_effect=['u', 'c', '123456789', 'John', '11/01/2000', '123 Pine St', 'c', '123456789', 'q', 'q'])
    @patch('sys.stdout', new_callable=StringIO)
    def test03_manage_users_create_user_already_exists(self, mock_output, mock_input):
        main()
        self.assertIn(ERROR_USER_ALREADY_EXISTS, mock_output.getvalue())

# ##############################################################################
# ░█▀▀█ █▀▀ █▀▀ █▀▀█ █░░█ █▀▀▄ ▀▀█▀▀ █▀▀ 
# ▒█▄▄█ █░░ █░░ █░░█ █░░█ █░░█ ░░█░░ ▀▀█ 
# ▒█░▒█ ▀▀▀ ▀▀▀ ▀▀▀▀ ░▀▀▀ ▀░░▀ ░░▀░░ ▀▀▀
# ##############################################################################

    @patch('builtins.input', side_effect=['c', 'c', '123456789', 'q', 'q'])
    @patch('sys.stdout', new_callable=StringIO)
    def test04_manage_accounts_create_account_user_not_found(self, mock_output, mock_input):
        main()
        self.assertIn(ERROR_USER_NOT_FOUND, mock_output.getvalue())

    @patch('builtins.input', side_effect=['u', 'c', '123456789', 'John', '11/01/2000', 'Rua A, 123', 'q', 'c', 'c', '123456789', 'q', 'q'])
    @patch('sys.stdout', new_callable=StringIO)
    def test05_manage_accounts_create_account(self, mock_output, mock_input):
        main()
        self.assertIn(MSG_USER_CREATED, mock_output.getvalue())
        self.assertIn(MSG_ACCOUNT_CREATED, mock_output.getvalue())
        self.assertIn("Branch: " + BRANCH, mock_output.getvalue())
        self.assertIn("Account: 1", mock_output.getvalue())
        self.assertIn("Holder: John - 123456789", mock_output.getvalue())


# ##############################################################################
# ▒█▀▀█ █░░█ █▀▀ █▀▀ █░█ ░▀░ █▀▀▄ █▀▀▀ 　 ░█▀▀█ █▀▀ █▀▀ █▀▀█ █░░█ █▀▀▄ ▀▀█▀▀ 
# ▒█░░░ █▀▀█ █▀▀ █░░ █▀▄ ▀█▀ █░░█ █░▀█ 　 ▒█▄▄█ █░░ █░░ █░░█ █░░█ █░░█ ░░█░░ 
# ▒█▄▄█ ▀░░▀ ▀▀▀ ▀▀▀ ▀░▀ ▀▀▀ ▀░░▀ ▀▀▀▀ 　 ▒█░▒█ ▀▀▀ ▀▀▀ ▀▀▀▀ ░▀▀▀ ▀░░▀ ░░▀░░
# ##############################################################################

    @patch('builtins.input', side_effect=['a', 'd', '200', 's', 'q', 'q'])
    @patch('sys.stdout', new_callable=StringIO)
    def test06_deposit(self, mock_output, mock_input):
        main()
        self.assertIn("Deposit     -     200.00 USD", mock_output.getvalue())
        self.assertIn("Net Balance -     200.00 USD", mock_output.getvalue())

    @patch('builtins.input', side_effect=['a', 'd', '200', 'w', '200', 's', 'q', 'q'])
    @patch('sys.stdout', new_callable=StringIO)
    def test07_withdraw(self, mock_output, mock_input):
        main()
        self.assertIn("Deposit     -     200.00 USD", mock_output.getvalue())
        self.assertIn("Withdraw    -    -200.00 USD", mock_output.getvalue())
        self.assertIn("Net Balance -       0.00 USD", mock_output.getvalue())

    @patch('builtins.input', side_effect=['a', 'd', '600', 'w', f'{WITHDRAWAL_LIMIT_AMOUNT + 50.0}', 'w', '100', 'w', '200', 'w', '305', 'w', '295', 'w', 's', 'q', 'q'])
    @patch('sys.stdout', new_callable=StringIO)
    def test08_withdraws(self, mock_output, mock_input):
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
