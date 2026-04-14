class Player:
    def __init__(self, name, nickname, grade):
        self.name = name
        self.nickname = nickname
        self.grade = grade

    def __str__(self):
        return f"Player: {self.name}\nNickname: {self.nickname}\nGrade: {self.grade}"
