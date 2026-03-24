class Campus:
    def __init__(self):
        self.nome = ""
        self.cidade = ""
    
    def __str__(self):
        return f"Campus: {self.nome}"

class Estudante:
    def __init__(self):
        self.cpf = ""
        self.nome = ""
        self.data_nasc = ""
    
    def __str__(self):
        return f"Estudante: {self.nome}"
    
class Curso:
    def __init__(self):
        self.nome = ""
        self.duracao = 0
        self.periodo = ""
        self.campus = Campus
    
    def __str__(self):
        return f"Curso: {self.nome}"

class Turma:
    def __init__(self):
        self.curso = Curso
        self.ano_ingresso = 0
        self.min_matriculas = 0

class Matricula:
    def __init__(self):
        self.estudante = Estudante
        self.turma = Turma
        self.ra = ""
        self.data_matricula = ""
        self.quem_matriculou = ""

ifpr_pvai = Campus()
ifpr_pvai.nome = "Instituto Federal do Paraná - Campus Paranavaí"
ifpr_pvai.cidae = "Paranavaí"

joao = Estudante()
joao.cpf = "111.111.111.11"
joao.nome = "João Emanuel"
joao.data_nasc = "05/10/2009"

info = Curso()
info.nome = "Informática"
info.duracao = 4
info.periodo = "Matutino"
info.campus = ifpr_pvai

info3 = Turma()
info3.curso = info
info3.ano_ingresso = 2012
info3.min_matriculas = 200

matricula1 = Matricula()
matricula1.estudante = joao
matricula1.turma = info3
matricula1.ra = "123213121"
matricula1.data_matricula = "08/01/2024"
matricula1.quem_matriculou = "neymar jr"