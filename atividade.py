class Conta:
    def __init__(self, numero_conta, saldo, titular):
        self.numero_conta = numero_conta
        self.saldo = saldo
        self.titular = titular
    
    def __str__(self):
        return f"{self.titular}: R$ {self.saldo}"
    
    def depositar(self, valor_depositar):
        print("Depósito realizado com sucesso!")
        self.saldo = self.saldo + valor_depositar
        print(f"Novo saldo de {self.titular}: R$ {self.saldo}")
    
    def sacar(self, valor_sacar):
        if valor_sacar > self.saldo:
            print("Saldo insuficiente para saque")
        else:
            print("Saque realizado com sucesso!")
            self.saldo = self.saldo - valor_sacar
        print(f"Novo saldo de {self.titular}: R$ {self.saldo}")

    def transferir(self, valor, conta_destino):
        if valor > self.saldo:
            print("Saldo insuficiente para transferência!")
        else:
            self.saldo = self.saldo - valor
            conta_destino.saldo = conta_destino.saldo + valor
            print("Transferência realizada com sucesso!")
        print(f"Saldo de {self.titular}: R$ {self.saldo}")
        print(f"Saldo de {conta_destino.titular}: R$ {conta_destino.saldo}")

conta1 = Conta(1, 1000, "João")
conta2 = Conta(2, 500, "Maria")

print(f"Saldo inicial: \n{conta1}\n{conta2}")

conta1.depositar(200)
conta2.sacar(300)
conta1.transferir(400, conta2)

print(f"Saldo final: \n{conta1}\n{conta2}")