from player import Player

class Team:
    def __init__(self, name, game):
        self.name = name
        self.game = game
        self.players_list = []
    
    def __str__(self):
        return f"Team name: {self.name}\nGame: {self.game}\nPlayers: {self.listar_jogadores()}"
    
    def print_players(self):
        if len(self.players_list) == 0:
            print(f"No players in team")
        else:
            for player in self.players_list:
                print(f" - {player.name}")