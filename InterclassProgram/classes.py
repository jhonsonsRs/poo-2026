class Player:
    def __init__(self, name, nickname, grade):
        self.name = name
        self.nickname = nickname
        self.grade = grade
        self.have_team = False

    def __str__(self):
        return f"Player: {self.name}\nNickname: {self.nickname}\nClasse: {self.grade}"

class Team:
    def __init__(self, name, game):
        self.name = name
        self.game = game
        self.players_list = []
    
    def __str__(self):
        return f"Nome do Time: {self.name}\nJogo: {self.game}\nQuantidade de players: {len(self.players_list)}"
    
    def print_players(self):
        if len(self.players_list) == 0:
            print(f"No players in team")
        else:
            for player in self.players_list:
                print(f" - {player.name}")
    
    def add_player(self, player):
        self.players_list.append(player)

    def remove_player(self, player):
        self.players_list.remove(player)