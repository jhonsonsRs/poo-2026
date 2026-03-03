import random

valor = random.randint(1, 10)
print(valor)
numero = -1
while not (1 <= numero <= 10):
    numero = int(input("Digite o numero entre 1 e 10: "))

while not (numero == valor):
    numero = int(input("vc perdeu lixo, tenta dnv: "))

print("vc venceu")

numeros = [67] * 10
numeros[0] = 6777

numero = [1, 0] * 10
for y in numero:
    print(y)

for i in numeros:
    print(i)

cont = 0
while cont <= 10:
    print(cont)
    cont += 1

