historico = []

def realizar_saque(saldo, valor_desejado):
    global historico
    if valor_desejado > saldo:
        print(f"Não há saldo suficiente")
        return saldo
    else:
        saldo -= valor_desejado
        mensagem = f"Saque realizado no valor de {valor_desejado} reais"
        historico.append(mensagem)
        return saldo

def realizar_deposito(saldo, valor_desejado):
    global historico
    saldo += valor_desejado
    mensagem = f"Depósito realizado no valor de {valor_desejado} reais"
    historico.append(mensagem)
    return saldo

def mostrar_extrato(saldo):
    global historico
    for i in historico:
        print(i)
    print(saldo)
    
saldo = 1000.0

while(True):
    print("Opção 1 - Sacar")
    print("Opção 2 - Depositar")
    print("Opção 3 - Extrato")
    print("Opção 4 - Sair")
    op = int(input("Digite a opção: "))
    if op == 1:
        valor_desejado = float(input("Digite o valor desejado a sacar: "))
        saldo = realizar_saque(saldo, valor_desejado)
    elif op == 2:
        valor_desejado = float(input("Digite o valor desejado a ser depositado: "))
        saldo = realizar_deposito(saldo, valor_desejado)
    elif op == 3:
        mostrar_extrato(saldo)
    else:
        break