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
format: street, number - neighborhood - city/state abbreviation. Only the
numbers of the SSN should be stored. We cannot register 2 users with the same
SSN.

Create Checking Account
The program should store accounts in a list, an account consists of: agency,
account number and user. The account number is sequential, starting at 1. The
agency number is fixed: "0001". The user can have more than one account, but an
account belongs to only one user.

Tip
To link a user to an account, filter the user list by looking for the SSN 
number reported for each user in the list.
"""

CURRENCY = "USD"
WITHDRAWAL_LIMIT_AMOUNT = 500
WITHDRAWAL_LIMIT_COUNT = 3
STATEMENT_WIDTH = 28
STATEMENT_HEADER = "Statement".center(STATEMENT_WIDTH, "=")
SEPARATOR_LINE_BALANCE = "-" * STATEMENT_WIDTH

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
    print(f"\n\n{STATEMENT_HEADER}", end="")
    print(statement if len(statement) > 0 else "\nNo transactions.")
    print(f"{SEPARATOR_LINE_BALANCE}")
    print("{:<11} - {:>10.2f} {}".format("Net Balance", balance, CURRENCY))

def main():
    menu = """

    [d] Deposit
    [w] Withdraw
    [s] Statement
    [q] Quit

    => """

    balance = 0
    statement = ""
    number_of_withdrawals = 0

    while True:

        option = input(menu)

        if option == "d":
            amount = float(input("\n\nEnter the amount to deposit\n=> "))
            balance, statement_line = deposit(amount, balance)
            statement += statement_line

        elif option == "w":
            if exceeded_withdrawal_count(number_of_withdrawals):
                continue

            amount = float(input("\n\nEnter the amount to withdraw\n=> "))
            balance, number_of_withdrawals, statement_line = withdraw(amount=amount, balance=balance, number_of_withdrawals=number_of_withdrawals)
            statement += statement_line

        elif option == "s":
            view_statement(balance, statement=statement)

        elif option == "q":
            break

        else:
            print("Invalid operation, please select the desired operation again.")

if __name__ == '__main__':
    main()