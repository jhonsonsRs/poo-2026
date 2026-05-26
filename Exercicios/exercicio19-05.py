class Calculadora:
    def __init__(self, marca, modelo, ano):
        self.marca = marca
        self.modelo = modelo
        self.ano = ano

    def somar(self, a, b):
        return a + b
    
    def subtrair(self, a, b):
        return a - b
    
    def multiplicar(self, a, b):
        return a * b
    
    def dividir(self, a, b):
        if b != 0:
            return a / b
        else:
            return "Erro: Divisão por zero não é permitida."
        
        