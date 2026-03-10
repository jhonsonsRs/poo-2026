import os
comando_email = "git config user.email \"jemanuel.orlando@gmail.com\""
retorno1 = os.system(comando_email)
print(f"comando retornou: {retorno1}")

mensagem = input("Mensagem do commit: ")
while(len(mensagem) < 2):
    print("⚠️ Mensagem muito pequena 🤏")
    mensagem = input("Mensagem do commit: ")

comando1 = "git add *"
retorno2 = os.system(comando1)
print(f"comando retornou: {retorno2}")


comando2 = f"git commit -m \"{mensagem}\""
retorno3 = os.system(comando2)
print(f"comando retornou: {retorno3}")

comando3 = "git push"
retorno4 = os.system(comando3)
print(f"comando retornou: {retorno4}")



