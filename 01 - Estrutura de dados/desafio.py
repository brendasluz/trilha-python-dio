import textwrap
from abc import ABC, abstractmethod

# ===================== CLASSES =====================

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

class Transacao(ABC):
    def __init__(self, valor):
        self.valor = valor

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def registrar(self, conta):
        conta.depositar(self.valor)
        conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)

class Conta:
    def __init__(self, cliente, numero):
        self.saldo = 0
        self.numero = numero
        self.cliente = cliente
        self.historico = Historico()

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            print("\nDepósito realizado com sucesso.")
        else:
            print("\nOperação falhou! Valor inválido.")

    def sacar(self, valor):
        if valor > self.saldo:
            print("\nOperação falhou! Saldo insuficiente.")
            return False
        elif valor <= 0:
            print("\nOperação falhou! Valor inválido.")
            return False
        else:
            self.saldo -= valor
            print("\nSaque realizado com sucesso.")
            return True

    def exibir_extrato(self):
        print("\n================ EXTRATO ================")
        if not self.historico.transacoes:
            print("Não foram realizadas movimentações.")
        else:
            for t in self.historico.transacoes:
                tipo = t.__class__.__name__
                print(f"{tipo}:\tR$ {t.valor:.2f}")
        print(f"\nSaldo:\t\tR$ {self.saldo:.2f}")
        print("==========================================")

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, limite_saques=3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0

    def sacar(self, valor):
        if valor > self.saldo:
            print("\nOperação falhou! Saldo insuficiente.")
            return False
        elif valor > self.limite:
            print("\nOperação falhou! Valor excede o limite.")
            return False
        elif self.numero_saques >= self.limite_saques:
            print("\nOperação falhou! Limite de saques excedido.")
            return False
        elif valor <= 0:
            print("\nOperação falhou! Valor inválido.")
            return False
        else:
            self.saldo -= valor
            self.numero_saques += 1
            print("\nSaque realizado com sucesso.")
            return True

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.nascimento = nascimento
        self.cpf = cpf

# ===================== FUNÇÕES =====================

def menu():
    opcoes = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(opcoes))

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ").strip()
    if any(u.cpf == cpf for u in usuarios):
        print("\nJá existe usuário com esse CPF.")
        return

    nome = input("Nome completo: ")
    nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuario = PessoaFisica(nome, nascimento, cpf, endereco)
    usuarios.append(usuario)
    print("\nUsuário criado com sucesso.")

def encontrar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario.cpf == cpf:
            return usuario
    return None

def criar_conta(numero_conta, usuarios, contas):
    cpf = input("Informe o CPF do usuário: ").strip()
    usuario = encontrar_usuario(cpf, usuarios)

    if not usuario:
        print("\nUsuário não encontrado.")
        return

    conta = ContaCorrente(cliente=usuario, numero=numero_conta)
    usuario.adicionar_conta(conta)
    contas.append(conta)
    print("\nConta criada com sucesso.")

def listar_contas(contas):
    for conta in contas:
        print("=" * 50)
        print(f"Agência: 0001")
        print(f"C/C: {conta.numero}")
        print(f"Titular: {conta.cliente.nome}")

# ===================== EXECUÇÃO =====================

def main():
    usuarios = []
    contas = []
    numero_conta = 1

    while True:
        opcao = menu()

        if opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            criar_conta(numero_conta, usuarios, contas)
            numero_conta += 1

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao in ["d", "s", "e"]:
            cpf = input("Informe o CPF do titular: ").strip()
            usuario = encontrar_usuario(cpf, usuarios)

            if not usuario:
                print("\nUsuário não encontrado.")
                continue

            if not usuario.contas:
                print("\nUsuário não possui contas.")
                continue

            conta = usuario.contas[0]  # usando a primeira conta como padrão

            if opcao == "d":
                valor = float(input("Valor do depósito: "))
                transacao = Deposito(valor)
                usuario.realizar_transacao(conta, transacao)

            elif opcao == "s":
                valor = float(input("Valor do saque: "))
                transacao = Saque(valor)
                usuario.realizar_transacao(conta, transacao)

            elif opcao == "e":
                conta.exibir_extrato()

        elif opcao == "q":
            print("\nEncerrando o sistema. Até logo!")
            break

        else:
            print("\nOpção inválida. Tente novamente.")

main()
