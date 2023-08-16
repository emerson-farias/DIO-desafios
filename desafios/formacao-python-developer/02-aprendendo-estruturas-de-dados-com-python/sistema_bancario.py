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

import textwrap

AGENCIA = "0001"
MOEDA = "R$"
LIMITE_VALOR_SAQUE = 500
LIMITE_QUANTIDADE_SAQUES = 3
LARGURA_EXTRATO = 31
BARRA_EXTRATO = "Extrato".center(LARGURA_EXTRATO, "=")
BARRA_SEPARADORA_SALDO = "-" * LARGURA_EXTRATO
ERRO_JA_EXISTE_USUARIO = "ERRO: Já existe um usuário com este CPF."
ERRO_OPERACAO_INVALIDA = "ERRO: Operação inválida, por favor selecione novamente a operação desejada."
ERRO_USUARIO_NAO_ENCONTRADO = "ERRO: Usuário não encontrado."
MSG_USUARIO_CRIADO = "Usuário criado com sucesso."
MSG_CONTA_CRIADA = "Conta criada com sucesso"

# ##############################################################################
# ▒█░▒█ █▀▀ █░░█ █▀▀█ █▀▀█ ░▀░ █▀▀█ █▀▀ 
# ▒█░▒█ ▀▀█ █░░█ █▄▄█ █▄▄▀ ▀█▀ █░░█ ▀▀█ 
# ░▀▄▄▀ ▀▀▀ ░▀▀▀ ▀░░▀ ▀░▀▀ ▀▀▀ ▀▀▀▀ ▀▀▀ 
# ##############################################################################

def buscar_usuario(usuarios, *, cpf):
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            return usuario
    return None

def criar_usuario(usuarios, *, cpf, nome, data_nascimento, endereco):
    if buscar_usuario(usuarios, cpf=cpf):
        raise ValueError(ERRO_JA_EXISTE_USUARIO)

    novo_usuario = {
        'cpf': cpf,
        'nome': nome,
        'data_nascimento': data_nascimento,
        'endereco': endereco
    }
    usuarios.append(novo_usuario)
    return novo_usuario

def criar_usuario_ui(usuarios):
    cpf = input("\nInforme o CPF (somente números)\n=> ")

    if buscar_usuario(usuarios, cpf=cpf):
        print(ERRO_JA_EXISTE_USUARIO)
        return

    nome = input("\nInforme o nome completo\n=> ")
    data_nascimento = input("\nInforme a data de nascimento (dd/mm/aaaa)\n=> ")
    endereco = input("\nInforme o endereço (logradouro, número - bairro - cidade/sigla estado)\n=> ")
    usuario = criar_usuario(usuarios, cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco)
    print("\n" + MSG_USUARIO_CRIADO)

def listar_usuarios(usuarios):
    if len(usuarios) == 0:
        print("\nSem usuários.")
        return

    extrato_usuarios = []
    max_largura = 0
    for usuario in usuarios:
        extrato_usuario = textwrap.dedent(f"""\
            Nome: {usuario['nome']}
            CPF: {usuario['cpf']}
            Data de Nasc.: {usuario['data_nascimento']}
            Endereço: {usuario['endereco']}""")
        extrato_usuarios.append(extrato_usuario)
        max_largura = max(max(len(linha) for linha in extrato_usuario.splitlines()), max_largura)
    print()
    for extrato_usuario in extrato_usuarios:
        print("=" * max_largura)
        print(extrato_usuario)

def administrar_usuarios(usuarios):
    menu = """
    ======= MENU USUÁRIOS =========
    [c] Criar usuário
    [l] Listar usuários
    [q] Sair

    => """

    while True:

        opcao = input(textwrap.dedent(menu))

        if opcao == "c":
            criar_usuario_ui(usuarios)

        elif opcao == "l":
            listar_usuarios(usuarios)

        elif opcao == "q":
            break

        else:
            print(ERRO_OPERACAO_INVALIDA)

# ##############################################################################
# ▒█▀▀█ █▀▀█ █▀▀▄ ▀▀█▀▀ █▀▀█ █▀▀ 
# ▒█░░░ █░░█ █░░█ ░░█░░ █▄▄█ ▀▀█ 
# ▒█▄▄█ ▀▀▀▀ ▀░░▀ ░░▀░░ ▀░░▀ ▀▀▀ 
# ##############################################################################

def listar_contas(contas, *, numero=None):
    if len(contas) == 0:
        print("\nSem contas.")
        return

    listagem_contas = []
    max_largura = 0
    for conta in contas:
        descrever = True
        if numero:
            descrever = conta['numero'] == numero
        if descrever:
            descricao_conta = textwrap.dedent(f"""\
                Agência: {conta['agencia']}
                Conta: {conta['numero']}
                Titular: {conta['titular']['nome']} - {conta['titular']['cpf']}""")
            listagem_contas.append(descricao_conta)
            max_largura = max(max(len(linha) for linha in descricao_conta.splitlines()), max_largura)
    if len(listagem_contas) == 0:
        return

    print()
    for descricao_conta in listagem_contas:
        if len(listagem_contas) > 1:
            print("=" * max_largura)
        print(descricao_conta)

def criar_conta(usuarios, contas, *, agencia, cpf_titular):
    titular = buscar_usuario(usuarios, cpf=cpf_titular)
    if titular is None:
        raise ValueError(ERRO_USUARIO_NAO_ENCONTRADO)

    numero_conta = len(contas) + 1
    nova_conta = {
        'agencia': agencia,
        'numero': numero_conta,
        'titular': titular
    }
    contas.append(nova_conta)
    return nova_conta

def criar_conta_ui(usuarios, contas):
    cpf_titular = input("\nInforme o CPF do titular da conta (somente números)\n=> ")

    if buscar_usuario(usuarios, cpf=cpf_titular) is None:
        print(ERRO_USUARIO_NAO_ENCONTRADO)
        return

    conta = criar_conta(usuarios, contas, agencia=AGENCIA, cpf_titular=cpf_titular)
    print("\n" + MSG_CONTA_CRIADA + ":")
    listar_contas(contas, numero=conta['numero'])

def administrar_contas(usuarios, contas):
    menu = """
    ======== MENU CONTAS ==========
    [c] Criar conta
    [l] Listar contas
    [q] Sair

    => """

    while True:

        opcao = input(textwrap.dedent(menu))

        if opcao == "c":
            criar_conta_ui(usuarios, contas)

        elif opcao == "l":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print(ERRO_OPERACAO_INVALIDA)

# ##############################################################################
# ▒█▀▀█ █▀▀█ █▀▀▄ ▀▀█▀▀ █▀▀█ ░░ ▒█▀▀█ █▀▀█ █▀▀█ █▀▀█ █▀▀ █▀▀▄ ▀▀█▀▀ █▀▀ 
# ▒█░░░ █░░█ █░░█ ░░█░░ █▄▄█ ▀▀ ▒█░░░ █░░█ █▄▄▀ █▄▄▀ █▀▀ █░░█ ░░█░░ █▀▀ 
# ▒█▄▄█ ▀▀▀▀ ▀░░▀ ░░▀░░ ▀░░▀ ░░ ▒█▄▄█ ▀▀▀▀ ▀░▀▀ ▀░▀▀ ▀▀▀ ▀░░▀ ░░▀░░ ▀▀▀
# ##############################################################################

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
    print(f"\n{BARRA_EXTRATO}", end="")
    print(extrato if len(extrato) > 0 else "\nNão há lançamentos.")
    print(f"{BARRA_SEPARADORA_SALDO}")
    print("{:<8} - {} {:>10.2f}".format("Saldo", MOEDA, saldo))

def acessar_conta():
    menu = """
    ===== MENU CONTA-CORRENTE =====
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair

    => """

    saldo = 0
    extrato = ""
    numero_saques = 0

    while True:

        opcao = input(textwrap.dedent(menu))

        if opcao == "d":
            valor = float(input("\nInforme valor a depositar\n=> "))
            saldo, linha_extrato = depositar(valor, saldo)
            extrato += linha_extrato

        elif opcao == "s":
            if excedeu_quantidade_saques(numero_saques):
                continue

            valor = float(input("\nInforme valor a sacar\n=> "))
            saldo, numero_saques, linha_extrato = sacar(valor=valor, saldo=saldo, numero_saques=numero_saques)
            extrato += linha_extrato

        elif opcao == "e":
            visualizar_extrato(saldo, extrato=extrato)

        elif opcao == "q":
            break

        else:
            print(ERRO_OPERACAO_INVALIDA)

# ##############################################################################
# ▒█▀▄▀█ █▀▀█ ░▀░ █▀▀▄ 
# ▒█▒█▒█ █▄▄█ ▀█▀ █░░█ 
# ▒█░░▒█ ▀░░▀ ▀▀▀ ▀░░▀
# ##############################################################################

def main():
    menu = """
    ======= MENU PRINCIPAL ========
    [a] Acessar Conta-Corrente
    [u] Administrar Usuários
    [c] Administrar Contas-Corrente
    [q] Sair

    => """
    usuarios = []
    contas = []

    while True:

        opcao = input(textwrap.dedent(menu))

        if opcao == "a":
            acessar_conta()

        elif opcao == "u":
            administrar_usuarios(usuarios)

        elif opcao == "c":
            administrar_contas(usuarios, contas)

        elif opcao == "q":
            break

        else:
            print(ERRO_OPERACAO_INVALIDA)

if __name__ == '__main__':
    main()