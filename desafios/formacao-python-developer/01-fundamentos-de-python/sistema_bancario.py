"""Desafio: Criando um sistema bancário
(extraído de https://academiapme-my.sharepoint.com/:p:/g/personal/kawan_dio_me/Ef-dMEJYq9BPotZQso7LUCwBJd7gDqCC2SYlUYx0ayrGNQ?e=G79e2L)

Objetivo Geral
--------------

Criar um sistema bancário com as operações: sacar, depositar e
visualizar extrato.

Desafio
-------
 
Fomos contratados por um grande banco para desenvolver o seu
novo sistema. Esse banco deseja modernizar suas operações e
para isso escolheu a linguagem Python. Para a primeira versão
do sistema devemos implementar apenas 3 operações: depósito,
saque e extrato.
 
Operação de depósito
--------------------

Deve ser possível depositar valores positivos para a minha conta
bancária. A v1 do projeto trabalha apenas com 1 usuário, dessa
forma não precisamos nos preocupar em identificar qual é o
número da agência e conta bancária. Todos os depósitos devem
ser armazenados em uma variável e exibidos na operação de
extrato.

Operação de saque
-----------------

O sistema deve permitir realizar 3 saques diários com limite
máximo de R$ 500,00 por saque. Caso o usuário não tenha saldo
em conta, o sistema deve exibir uma mensagem informando que não
será possível sacar o dinheiro por falta de saldo. Todos os
saques devem ser armazenados em uma variável e exibidos na
operação de extrato.

Operação de extrato
-------------------

Essa operação deve listar todos os depósitos e saques realizados
na conta. No fim da listagem deve ser exibido o saldo atual da
conta. Se o extrato estiver em branco, exibir a mensagem:Não
foram realizadas movimentações.

Os valores devem ser exibidos utilizando o formato R$ xxx.xx,
exemplo:

1500.45 = R$ 1500.45
"""

menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

MOEDA = "R$"
LIMITE_VALOR_SAQUE = 500
LIMITE_QUANTIDADE_SAQUES = 3
OPERACOES_DICT = {
    "d": "Depósito",
    "s": "Saque"
}
LARGURA_EXTRATO = 26
BARRA_EXTRATO = "Extrato".center(LARGURA_EXTRATO, "=")
BARRA_SEPARADORA_SALDO = "-" * LARGURA_EXTRATO

saldo = 0
extrato = ""
numero_saques = 0

while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("\n\nInforme valor a depositar\n=> "))
        if valor <= 0:
            print("ERRO: Valor a depositar inválido. Favor informar valor positivo.")
            continue
        
        saldo += valor
        extrato += f"\n{OPERACOES_DICT[opcao]:<8} - {MOEDA} {valor:>10.2f} C"

    elif opcao == "s":
        excedeu_quantidade_saques = numero_saques >= LIMITE_QUANTIDADE_SAQUES
        if excedeu_quantidade_saques:
            print(f"ERRO: Quantidade limite de saques diários excedido ({LIMITE_QUANTIDADE_SAQUES}). Favor tentar no próximo dia.")
            continue

        valor = float(input("\n\nInforme valor a sacar\n=> "))
        if valor <= 0:
            print("ERRO: Valor a sacar inválido. Favor informar valor positivo.")
            continue

        excedeu_valor_saque = valor > LIMITE_VALOR_SAQUE
        saldo_insuficiente = valor > saldo

        if excedeu_valor_saque:
            print(f"ERRO: Valor maior que limite de saque permitido ({MOEDA} {LIMITE_VALOR_SAQUE:.2f}).")
        elif saldo_insuficiente:
            print("ERRO: Saldo insuficiente.")
        else:
            saldo -= valor
            numero_saques += 1
            extrato += f"\n{OPERACOES_DICT[opcao]:<8} - {MOEDA} {valor:>10.2f} D"

    elif opcao == "e":
        print(f"\n\n{BARRA_EXTRATO}", end="")
        print(extrato if len(extrato) > 0 else "\nNão há lançamentos.")
        print(f"{BARRA_SEPARADORA_SALDO}")
        print("{:<8} - {} {:>10.2f}".format("Saldo", MOEDA, saldo))

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")