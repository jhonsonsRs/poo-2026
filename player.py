class Player:
    def __init__(self, name, damage, hp):
        self.name = name
        self.damage = damage
        self.hp = hp
    
    def attack(self):
        print(f"{self.name} attacked")

class Slime:
    def __init__(self, name, damage):
        pass

vetor = [1, 2, 3, 4, 5, 6, 7, 8 ,9, 10]

for i in vetor:
    print(i)
