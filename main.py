nome = input("Nome: ")
idade = int(input("Idade: "))
salario = float(input("Salário: R$"))

print(f"Olá {nome}. Você tem {idade} anos")
if salario <= 10000:
    print(f"você ganha mal. R$ {salario}")
elif salario > 10000 and salario < 20000:
    print(f"você ganha bem. R$ {salario}")
else: 
    print(f"você ganha muito bem. R$ {salario}")