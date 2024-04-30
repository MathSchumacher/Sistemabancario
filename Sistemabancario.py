import datetime
import json

menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

# Inicializa ou carrega os dados do programa
def carregar_dados():
    try:
        with open("dados.json", "r") as file:
            dados = json.load(file)
            return dados
    except FileNotFoundError:
        return {
            "saldo": 0,
            "extrato": "",
            "numero_saques": 0,
            "ultima_operacao": None
        }

def salvar_dados(dados):
    with open("dados.json", "w") as file:
        json.dump(dados, file)

# Função para verificar se os saques devem ser redefinidos
def verificar_redefinicao(dados):
    ultima_operacao = dados["ultima_operacao"]
    if ultima_operacao is not None:
        ultima_operacao = datetime.datetime.strptime(ultima_operacao, "%Y-%m-%d %H:%M:%S")
        agora = datetime.datetime.now()
        diferenca_tempo = agora - ultima_operacao
        if diferenca_tempo.total_seconds() >= 86400:  # 24 horas em segundos
            dados["numero_saques"] = 0
            dados["ultima_operacao"] = agora.strftime("%Y-%m-%d %H:%M:%S")
            salvar_dados(dados)

# Carrega os dados iniciais
dados = carregar_dados()

while True:
    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))
        if valor > 0:
            dados["saldo"] += valor
            dados["extrato"] += f"Depósito: R$ {valor:.2f}\n"
            dados["ultima_operacao"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            salvar_dados(dados)
        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "s":
        verificar_redefinicao(dados)  # Verifica se os saques devem ser redefinidos

        valor = float(input("Informe o valor do saque: "))

        excedeu_saldo = valor > dados["saldo"]
        excedeu_limite = valor > 500
        excedeu_saques = dados["numero_saques"] >= 3

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")

        elif valor > 0:
            dados["saldo"] -= valor
            dados["extrato"] += f"Saque: R$ {valor:.2f}\n"
            dados["numero_saques"] += 1
            dados["ultima_operacao"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            salvar_dados(dados)

        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "e":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not dados["extrato"] else dados["extrato"])
        print(f"\nSaldo: R$ {dados['saldo']:.2f}")
        print("==========================================")

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
