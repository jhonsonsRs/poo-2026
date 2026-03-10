def criar_media(n1, n2, n3):
    return (n1 + n2 + n3) / 3

alunos = []
medias = []
for i in range(0, 5):
    nome = input("Digite o nome do aluno: ")
    nota1 = int(input("Nota 1: "))
    nota2 = int(input("Nota 2: "))
    nota3 = int(input("Nota 3: "))
    media = criar_media(nota1, nota2, nota3)
    alunos.append(nome)
    medias.append(media)

for y in range(0, len(alunos)):
    print(f"Aluno {alunos[y]}, média: {medias[y]}")
    if medias[y] >= 7.0:
        print("Aluno aprovado")
    else:
        print("Aluno reprovado")