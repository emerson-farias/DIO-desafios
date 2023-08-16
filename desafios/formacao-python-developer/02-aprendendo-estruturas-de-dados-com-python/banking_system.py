"""Challenge: Creating a Banking System (continuation)
(original challenge - https://academiapme-my.sharepoint.com/:p:/g/personal/kawan_dio_me/Ef-dMEJYq9BPotZQso7LUCwBJd7gDqCC2SYlUYx0ayrGNQ?e=G79e2L;
continuation as explained in https://web.dio.me/project/optimizing-the-banking-system-with-python-functions/learning/82a55799-cfb8-479d-85a3-4982e29c90ba?back=/track/formacao-python-developer&tab=undefined&moduleId=undefined)

General Objective
-----------------

Separate the existing withdrawal, deposit and statement functions. Create two
new functions: user (client) registration and bank account registration.

Challenge
---------

We need to make our code more modular; for this, we will create functions
for the existing operations: withdraw, deposit, and view history. Moreover,
for version 2 of our system, we need to create two new functions: create a user 
(bank client) and create a checking account (link with the user).

Function Separation
-------------------

We should create functions for all system operations. To exercise everything we
learned in this module, each function will have a rule in the passage of
arguments. The return and how they will be called can be defined by you in the
way you think is best.

Withdrawal
----------

The withdrawal function should receive arguments only by name (keyword only).
Suggestion of arguments: balance, value, statement, limit, number_withdrawals,
withdrawal_limit. Suggestion of return: balance and statement.

Deposit
-------

The deposit function should receive arguments only by position (positional
only). Suggestion of arguments: balance, value, statement. Suggestion of return:
balance and statement.

Statement
---------

The statement function must receive arguments by position and name (positional
only and keyword only). Named arguments: statement.

New Functions
-------------

We need to create two new functions: create user and create checking account.
Feel free to add more functions, list accounts.

Create User (Client)
--------------------

The program should store users in a list, a user is composed of: name, date of
birth, SSN (Social Security Number), and address. The address is a string in the
format: street number and name, apt/suite (if appl.) - city, state abbreviation.
Only the numbers of the SSN should be stored. We cannot register 2 users with
the same SSN.

Create Checking Account
-----------------------

The program should store accounts in a list, an account consists of: branch
number, account number and user. The account number is sequential, starting at
1. The branch number is fixed: "0001". The user can have more than one account,
but an account belongs to only one user.

Tip
---

To link a user to an account, filter the user list by looking for the SSN number
reported for each user in the list.
"""

import textwrap

BRANCH = "0001"
CURRENCY = "USD"
WITHDRAWAL_LIMIT_AMOUNT = 500
WITHDRAWAL_LIMIT_COUNT = 3
STATEMENT_WIDTH = 29
STATEMENT_HEADER = "Statement".center(STATEMENT_WIDTH, "=")
SEPARATOR_LINE_BALANCE = "-" * STATEMENT_WIDTH
ERROR_USER_ALREADY_EXISTS = "ERROR: A user with this SSN already exists."
ERROR_INVALID_OPERATION = "ERROR: Invalid operation, please select the desired operation again."
MSG_USER_CREATED = "User created successfully."

# ##############################################################################
# ▒█░▒█ █▀▀ █▀▀ █▀▀█ █▀▀ 
# ▒█░▒█ ▀▀█ █▀▀ █▄▄▀ ▀▀█ 
# ░▀▄▄▀ ▀▀▀ ▀▀▀ ▀░▀▀ ▀▀▀
# ##############################################################################

def search_user(users, *, ssn):
    for user in users:
        if user['ssn'] == ssn:
            return user
    return None

def create_user(users, *, ssn, name, birth_date, address):
    if search_user(users, ssn=ssn):
        raise ValueError(ERROR_USER_ALREADY_EXISTS)

    new_user = {
        'ssn': ssn,
        'name': name,
        'birth_date': birth_date,
        'address': address
    }
    users.append(new_user)
    return new_user

def create_user_ui(users):
    ssn = input("\nEnter the SSN (numbers only)\n=> ")

    if search_user(users, ssn=ssn):
        print(ERROR_USER_ALREADY_EXISTS)
        return

    name = input("\nEnter the full name\n=> ")
    birth_date = input("\nEnter the birth date (mm/dd/aaaa)\n=> ")
    address = input("\nEnter the address (street number and name, apt/suite [if appl.] - city, state abbreviation)\n=> ")
    user = create_user(users, ssn=ssn, name=name, birth_date=birth_date, address=address)
    print("\n" + MSG_USER_CREATED)

def list_users(users):
    if len(users) == 0:
        print("\nNo users.")
        return

    user_statements = []
    max_width = 0
    for user in users:
        user_statement = textwrap.dedent(f"""\
            Name: {user['name']}
            SSN: {user['ssn']}
            Birth Date: {user['birth_date']}
            Address: {user['address']}""")
        user_statements.append(user_statement)
        max_width = max(max(len(line) for line in user_statement.splitlines()), max_width)
    print()
    for user_statement in user_statements:
        print("=" * max_width)
        print(user_statement)

def manage_users(users):
    menu = """
    ======== USERS MENU =========
    [c] Create users
    [l] List users
    [q] Quit

    => """

    while True:

        option = input(textwrap.dedent(menu))

        if option == "c":
            create_user_ui(users)

        elif option == "l":
            list_users(users)

        elif option == "q":
            break

        else:
            print(ERROR_INVALID_OPERATION)

# ##############################################################################
# ░█▀▀█ █▀▀ █▀▀ █▀▀█ █░░█ █▀▀▄ ▀▀█▀▀ █▀▀ 
# ▒█▄▄█ █░░ █░░ █░░█ █░░█ █░░█ ░░█░░ ▀▀█ 
# ▒█░▒█ ▀▀▀ ▀▀▀ ▀▀▀▀ ░▀▀▀ ▀░░▀ ░░▀░░ ▀▀▀
# ##############################################################################

def manage_accounts():
    menu = """
    ======= ACCOUNTS MENU =======
    [c] Create account
    [l] List accounts
    [q] Quit

    => """

    while True:

        option = input(textwrap.dedent(menu))

        if option == "c":
            pass

        elif option == "l":
            pass

        elif option == "q":
            break

        else:
            print(ERROR_INVALID_OPERATION)

# ##############################################################################
# ▒█▀▀█ █░░█ █▀▀ █▀▀ █░█ ░▀░ █▀▀▄ █▀▀▀ 　 ░█▀▀█ █▀▀ █▀▀ █▀▀█ █░░█ █▀▀▄ ▀▀█▀▀ 
# ▒█░░░ █▀▀█ █▀▀ █░░ █▀▄ ▀█▀ █░░█ █░▀█ 　 ▒█▄▄█ █░░ █░░ █░░█ █░░█ █░░█ ░░█░░ 
# ▒█▄▄█ ▀░░▀ ▀▀▀ ▀▀▀ ▀░▀ ▀▀▀ ▀░░▀ ▀▀▀▀ 　 ▒█░▒█ ▀▀▀ ▀▀▀ ▀▀▀▀ ░▀▀▀ ▀░░▀ ░░▀░░
# ##############################################################################

def exceeded_withdrawal_count(number_of_withdrawals):
    if number_of_withdrawals >= WITHDRAWAL_LIMIT_COUNT:
        print(f"ERROR: Daily withdrawal limit exceeded ({WITHDRAWAL_LIMIT_COUNT}). Please try again tomorrow.")
        return True
    return False

# The withdrawal function should receive arguments only by name (keyword only).
def withdraw(*, amount, balance, number_of_withdrawals):
    if amount <= 0:
        print("ERROR: Invalid withdrawal amount. Please enter a positive value.")
        return balance, number_of_withdrawals, ""
    
    exceeded_withdrawal_amount = amount > WITHDRAWAL_LIMIT_AMOUNT
    if exceeded_withdrawal_amount:
        print(f"ERROR: Amount exceeds allowed withdrawal limit ({WITHDRAWAL_LIMIT_AMOUNT:.2f} {CURRENCY}).")
        return balance, number_of_withdrawals, ""

    insufficient_balance = amount > balance
    if insufficient_balance:
        print("ERROR: Insufficient balance.")
        return balance, number_of_withdrawals, ""

    balance -= amount
    number_of_withdrawals += 1
    formatted_amount = f"{amount:>10.2f}"
    formatted_amount = f"{' ' * (9 - len(formatted_amount.strip()))}-" + formatted_amount.strip()
    operation = "Withdraw"
    statement_line = f"\n{operation:<11} - {formatted_amount} {CURRENCY}"
    return balance, number_of_withdrawals, statement_line

# The deposit function should receive arguments only by position (positional only).
def deposit(amount, balance):
    if amount <= 0:
        print("ERROR: Invalid deposit amount. Please enter a positive value.")
        return balance, ""
    balance += amount
    operation = "Deposit"
    statement_line = f"\n{operation:<11} - {amount:>10.2f} {CURRENCY}"
    return balance, statement_line

# The statement function must receive arguments by position and name (positional
# only and keyword only). Named arguments: statement.
def view_statement(balance, *, statement):
    print(f"\n{STATEMENT_HEADER}", end="")
    print(statement if len(statement) > 0 else "\nNo transactions.")
    print(f"{SEPARATOR_LINE_BALANCE}")
    print("{:<11} - {:>10.2f} {}".format("Net Balance", balance, CURRENCY))

def access_account():
    menu = """
    === CHECKING ACCOUNT MENU ===
    [d] Deposit
    [w] Withdraw
    [s] Statement
    [q] Quit

    => """

    balance = 0
    statement = ""
    number_of_withdrawals = 0

    while True:

        option = input(textwrap.dedent(menu))

        if option == "d":
            amount = float(input("\nEnter the amount to deposit\n=> "))
            balance, statement_line = deposit(amount, balance)
            statement += statement_line

        elif option == "w":
            if exceeded_withdrawal_count(number_of_withdrawals):
                continue

            amount = float(input("\nEnter the amount to withdraw\n=> "))
            balance, number_of_withdrawals, statement_line = withdraw(amount=amount, balance=balance, number_of_withdrawals=number_of_withdrawals)
            statement += statement_line

        elif option == "s":
            view_statement(balance, statement=statement)

        elif option == "q":
            break

        else:
            print(ERROR_INVALID_OPERATION)

# ##############################################################################
# ▒█▀▄▀█ █▀▀█ ░▀░ █▀▀▄ 
# ▒█▒█▒█ █▄▄█ ▀█▀ █░░█ 
# ▒█░░▒█ ▀░░▀ ▀▀▀ ▀░░▀
# ##############################################################################

def main():
    menu = """
    ========= MAIN MENU =========
    [a] Access Checking Account
    [u] Manage Users
    [c] Manage Checking Accounts
    [q] Quit

    => """
    users = []
    accounts = []

    while True:

        option = input(textwrap.dedent(menu))

        if option == "a":
            access_account()

        elif option == "u":
            manage_users(users)

        elif option == "c":
            manage_accounts()

        elif option == "q":
            break

        else:
            print(ERROR_INVALID_OPERATION)

if __name__ == '__main__':
    main()