"""Challenge: Creating a Banking System
(extracted from https://academiapme-my.sharepoint.com/:p:/g/personal/kawan_dio_me/Ef-dMEJYq9BPotZQso7LUCwBJd7gDqCC2SYlUYx0ayrGNQ?e=G79e2L)

General Objective
-----------------

Create a banking system with the operations: withdraw, deposit, and view
statement.

Challenge
---------

We have been hired by a large bank to develop its new system. This bank wants
to modernize its operations and for that, it chose the Python language. For the
first version of the system, we must implement only 3 operations: deposit,
withdraw, and statement.

Deposit Operation
-----------------

It should be possible to deposit positive values into my bank account. Version 1
of the project only works with 1 user, so we don't need to worry about
identifying the bank branch and account number. All deposits must be stored in
a variable and displayed in the statement operation.

Withdrawal Operation
--------------------

The system must allow 3 daily withdrawals with a maximum limit of 500.00 USD per
withdrawal. If the user does not have a balance in the account, the system must
display a message stating that it will not be possible to withdraw money due to
a lack of funds. All withdrawals must be stored in a variable and displayed in
the statement operation.

Statement Operation
-------------------

This operation must list all deposits and withdrawals made in the account. At
the end of the listing, the current balance of the account must be displayed. If
the statement is blank, display the message: No transactions were made.

Values must be displayed using the format xxx.xx USD, example:

1500.45 = 1500.45 USD
"""

menu = """

[d] Deposit
[w] Withdraw
[s] Statement
[q] Quit

=> """

CURRENCY = "USD"
WITHDRAWAL_LIMIT_AMOUNT = 500
WITHDRAWAL_LIMIT_COUNT = 3
OPERATIONS_DICT = {
    "d": "Deposit",
    "w": "Withdraw"
}
STATEMENT_WIDTH = 28
STATEMENT_HEADER = "Statement".center(STATEMENT_WIDTH, "=")
SEPARATOR_LINE_BALANCE = "-" * STATEMENT_WIDTH

balance = 0
statement = ""
number_of_withdrawals = 0

while True:

    option = input(menu)

    if option == "d":
        amount = float(input("\n\nEnter the amount to deposit\n=> "))
        if amount <= 0:
            print("ERROR: Invalid deposit amount. Please enter a positive value.")
            continue
        
        balance += amount
        statement += f"\n{OPERATIONS_DICT[option]:<11} - {amount:>10.2f} {CURRENCY}"

    elif option == "w":
        exceeded_withdrawal_count = number_of_withdrawals >= WITHDRAWAL_LIMIT_COUNT
        if exceeded_withdrawal_count:
            print(f"ERROR: Daily withdrawal limit exceeded ({WITHDRAWAL_LIMIT_COUNT}). Please try again tomorrow.")
            continue

        amount = float(input("\n\nEnter the amount to withdraw\n=> "))
        if amount <= 0:
            print("ERROR: Invalid withdrawal amount. Please enter a positive value.")
            continue

        exceeded_withdrawal_amount = amount > WITHDRAWAL_LIMIT_AMOUNT
        insufficient_balance = amount > balance

        if exceeded_withdrawal_amount:
            print(f"ERROR: Amount exceeds allowed withdrawal limit ({WITHDRAWAL_LIMIT_AMOUNT:.2f} {CURRENCY}).")
        elif insufficient_balance:
            print("ERROR: Insufficient balance.")
        else:
            balance -= amount
            number_of_withdrawals += 1
            formatted_amount = f"{amount:>10.2f}"
            formatted_amount = f"{' ' * (9 - len(formatted_amount.strip()))}-" + formatted_amount.strip()
            statement += f"\n{OPERATIONS_DICT[option]:<11} - {formatted_amount} {CURRENCY}"

    elif option == "s":
        print(f"\n\n{STATEMENT_HEADER}", end="")
        print(statement if len(statement) > 0 else "\nNo transactions.")
        print(f"{SEPARATOR_LINE_BALANCE}")
        print("{:<11} - {:>10.2f} {}".format("Net Balance", balance, CURRENCY))

    elif option == "q":
        break

    else:
        print("Invalid operation, please select the desired operation again.")