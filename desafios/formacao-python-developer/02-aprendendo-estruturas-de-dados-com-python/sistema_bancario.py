"""Desafio: Criando um sistema bancário (continuação)
(desafio original - https://academiapme-my.sharepoint.com/:p:/g/personal/kawan_dio_me/Ef-dMEJYq9BPotZQso7LUCwBJd7gDqCC2SYlUYx0ayrGNQ?e=G79e2L;
continuação cfe. explicado em https://web.dio.me/project/otimizando-o-sistema-bancario-com-funcoes-python/learning/82a55799-cfb8-479d-85a3-4982e29c90ba?back=/track/formacao-python-developer&tab=undefined&moduleId=undefined)

Objetivo Geral
--------------

Separar as funções existentes de saque, depósito e extrato em funções. Criar
duas novas funções: cadastrar usuário (cliente) e cadastrar conta bancária.

Desafio
-------

Precisamos deixar nosso código mais modularizado, para isso vamos criar funções
para as operações existentes: sacar, depositar e visualizar histórico. Além
disso, para a versão 2 do nosso sistema, precisamos criar duas novas funções:
criar usuário (cliente do banco) e criar conta corrente (vincular com usuário).

Separação em funções
--------------------

Devemos criar funções para todas as operações do sistema. Para exercitar tudo o
que aprendemos neste módulo, cada função vai ter uma regra na passagem de
argumentos. O retorno e a forma como serão chamadas, pode ser definida por você
da forma que achar melhor.

Saque
-----

A função saque deve receber os argumentos apenas por nome (keyword only).
Sugestão de argumentos: saldo, valor, extrato, limite, numero_saques,
limite_saques. Sugestão de retorno: saldo e extrato.

Depósito
--------

A função depósito deve receber os argumentos apenas por posição (positional
only). Sugestão de argumentos: saldo, valor, extrato. Sugestão de retorno: saldo
e extrato.

Extrato
-------

A função extrato deve receber os argumentos por posição e nome (positional only
e keyword only). Argumentos nomeados: extrato.

Novas funções
-------------

Precisamos criar duas novas funções: criar usuário e criar conta corrente. Fique
à vontade para adicionar mais funções, listar contas.

Criar usuário (cliente)
-----------------------

O programa deve armazenar os usuários em uma lista, um usuário é composto por:
nome, data de nascimento, CPF e endereço. O endereço é uma string com o formato:
logradouro, número - bairro - cidade/sigla estado. Deve ser armazenado somente
os números do CPF. Não podemos cadastrar 2 usuários com o mesmo CPF.

Criar conta corrente
--------------------

O programa deve armazenar contas em uma lista, uma conta é composta por: agência,
número da conta e usuário. O número da conta é sequencial, iniciando em 1. O
número da agência é fixo: "0001". O usuário pode ter mais de uma conta, mas uma
conta pertence a somente um usuário.

Dica
----

Para vincular um usuário a uma conta, filtre a lista de usuários buscando o
número do CPF informado para cada usuário da lista.
"""

MOEDA = "R$"
LIMITE_VALOR_SAQUE = 500
LIMITE_QUANTIDADE_SAQUES = 3
LARGURA_EXTRATO = 26
BARRA_EXTRATO = "Extrato".center(LARGURA_EXTRATO, "=")
BARRA_SEPARADORA_SALDO = "-" * LARGURA_EXTRATO

def excedeu_quantidade_saques(numero_saques):
    if numero_saques >= LIMITE_QUANTIDADE_SAQUES:
        print(f"ERRO: Quantidade limite de saques diários excedido ({LIMITE_QUANTIDADE_SAQUES}). Favor tentar no próximo dia.")
        return True
    return False

# A função saque deve receber os argumentos apenas por nome (keyword only).
def sacar(*, valor, saldo, numero_saques):
    if valor <= 0:
        print("ERRO: Valor a sacar inválido. Favor informar valor positivo.")
        return saldo, numero_saques, ""
    
    excedeu_valor_saque = valor > LIMITE_VALOR_SAQUE
    if excedeu_valor_saque:
        print(f"ERRO: Valor maior que limite de saque permitido ({MOEDA} {LIMITE_VALOR_SAQUE:.2f}).")
        return saldo, numero_saques, ""
    
    saldo_insuficiente = valor > saldo
    if saldo_insuficiente:
        print("ERRO: Saldo insuficiente.")
        return saldo, numero_saques, ""
    
    saldo -= valor
    numero_saques += 1
    operacao = "Saque"
    linha_extrato = f"\n{operacao:<8} - {MOEDA} {valor:>10.2f} D"
    return saldo, numero_saques, linha_extrato

# A função depósito deve receber os argumentos apenas por posição (positional only).
def depositar(valor, saldo):
    if valor <= 0:
        print("ERRO: Valor a depositar inválido. Favor informar valor positivo.")
        return saldo, ""
    
    saldo += valor
    operacao = "Depósito"
    linha_extrato = f"\n{operacao:<8} - {MOEDA} {valor:>10.2f} C"
    return saldo, linha_extrato

# A função extrato deve receber os argumentos por posição e nome (positional only
# e keyword only). Argumentos nomeados: extrato.
def visualizar_extrato(saldo, *, extrato):
    print(f"\n\n{BARRA_EXTRATO}", end="")
    print(extrato if len(extrato) > 0 else "\nNão há lançamentos.")
    print(f"{BARRA_SEPARADORA_SALDO}")
    print("{:<8} - {} {:>10.2f}".format("Saldo", MOEDA, saldo))

def main():
    menu = """

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair

    => """

    saldo = 0
    extrato = ""
    numero_saques = 0

    while True:

        opcao = input(menu)

        if opcao == "d":
            valor = float(input("\n\nInforme valor a depositar\n=> "))
            saldo, linha_extrato = depositar(valor, saldo)
            extrato += linha_extrato

        elif opcao == "s":
            if excedeu_quantidade_saques(numero_saques):
                continue

            valor = float(input("\n\nInforme valor a sacar\n=> "))
            saldo, numero_saques, linha_extrato = sacar(valor=valor, saldo=saldo, numero_saques=numero_saques)
            extrato += linha_extrato

        elif opcao == "e":
            visualizar_extrato(saldo, extrato=extrato)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == '__main__':
    main()