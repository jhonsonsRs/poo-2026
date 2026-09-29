from contato import Contato

def cadastrar_contato():
    nome = input("Digite o seu nome: ")
    telefone = input("Digite o seu telefone: ")
    Contato.create(
        nome=nome,
        telefone=telefone
    )
    print("Contato criado!")

def listar_contatos():
    contatos = Contato.select()
    if not contatos:
        print("\nNão existe nenhum contato.")
        return
    print("\nLISTA DE CONTATOS")
    for contato in contatos:
        print(contato)

def buscar_contato():
    nome = input("Digite o nome completo do contato que deseja buscar: ")
    contato = Contato.get_or_none(
        Contato.nome.contains(nome)
    )
    if contato:
        print(contato)
    else:
        print("Contato não encontrado")

def editar_contato():
    id = input("Digite o id do contato:")
    contato = Contato.get_or_none(
        Contato.id == id
    )
    if contato:
        nome_novo = input("Digite o novo nome do contato ou vazio: ")
        if nome_novo:
            contato.nome = nome_novo
        telefone_novo = input("Digite o novo telefone do contato ou vazio: ")
        if telefone_novo:
            contato.telefone = telefone_novo
        contato.save()
    else:
        print("O contato não existe.")

def remover_contato():
    id = input("Digite o id do contato:")
    contato = Contato.get_or_none(
        Contato.id == id
    )
    if contato:
        contato.delete_instance()
        print("Removido")
    else:
        print("Contato não existe")

while True:
    print("\n===== AGENDA DE CONTATOS =====")
    print("1 - Cadastrar contato")
    print("2 - Ver todos os contatos")
    print("3 - Buscar contato pelo nome")
    print("4 - Editar contato pelo ID")
    print("5 - Excluir contato pelo ID")
    print("6 - Sair")
    opcao = int(input("\nEscolha uma opção: "))
    if opcao == 1:
        cadastrar_contato()
    elif opcao == 2:
        listar_contatos()
    elif opcao == 3:
        buscar_contato()
    elif opcao == 4:
        editar_contato()
    elif opcao == 5:
        remover_contato()
    elif opcao == 6:
        print("Saindo do programa...")
        break
    else:
        print("Opção inválida, por favor digite uma opção válida")