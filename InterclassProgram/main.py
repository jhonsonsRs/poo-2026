from classes import Player, Team

players_list = []
teams_list = []

def register_player():
    name = input("Digite o nome do jogador: ")
    nickname = input("Digite o nickname do jogador: ")
    grade = input("Digite a classe escolar do jogador: ")
    for player in players_list:
        if player.nickname == nickname:
            print(f"Nickname '{nickname}' já está em uso! Por favor, escolha outro.")
            return
    player = Player(name, nickname, grade)
    players_list.append(player)

def register_team():
    name = input("Digite o nome da equipe: ")
    game = input("Digite o nome do jogo que a equipe irá competir: ")
    team = Team(name, game)
    teams_list.append(team)

def add_player_team():
    player_name = input("Digite o nome do jogador: ")
    team_name = input("Digite o nome do time: ")
    player_found = None
    for player in players_list:
        if player.name == player_name:
            if player.have_team:
                print(f"Jogador '{player_name}' já pertence a uma equipe!")
                return
            player_found = player
            break
    
    team_found = None
    for team in teams_list:
        if team.name == team_name:
            if len(team.players_list) >= 5:
                print("O time está cheio.")
                return
            team_found = team
            break
    
    if player_found and team_found:
        team_found.add_player(player_found)
        player_found.have_team = True
        print(f"{player_found.name} adicionado ao time {team_found.name}!")
    elif not player_found:
        print(f"Jogador '{player_name}' não encontrado!")
    elif not team_found:
        print(f"Equipe '{team_name}' não encontrada!")

def print_teams():
    for team in teams_list:
        print(team)

def print_players_team():
    team_name = input("Digite o nome da equipe: ")
    team_found = None
    for team in teams_list:
        if team.name == team_name:
            team_found = team
    if team_found:
        for players in team_found.players_list:
            print(players.name)
    else:
        print(f"Equipe '{team_name}' não encontrada!")

def remove_player_team():
    player_name = input("Digite o nome do jogador: ")
    team_name = input("Digite o nome do time: ")
    player_found = None
    for player in players_list:
        if player.name == player_name:
            if not player.have_team:
                print(f"Jogador '{player_name}' não pertence a nenhuma equipe!")
                return
            player_found = player
            break
    
    team_found = None
    for team in teams_list:
        if team.name == team_name:
            team_found = team
            break
    
    if player_found and team_found:
        team_found.remove_player(player_found)
        player_found.have_team = False
        print(f"{player_found.name} removido do time {team_found.name}!")
    elif not player_found:
        print(f"Jogador '{player_name}' não encontrado!")
    elif not team_found:
        print(f"Equipe '{team_name}' não encontrada!")

def search_player():
    nickname = input("Digite o nickname do jogador: ")
    player_found = None
    for player in players_list:
        if player.nickname == nickname:
            player_found = player
            break
    if player_found:
        print(player_found)
    else:
        print(f"Nickname '{nickname}' não encontrado!")

def print_menu():
    print("=" * 40)
    print("  CAMPEONATO INTERCLASSE DE E-SPORTS")
    print("=" * 40)
    print("1. Cadastrar jogador")
    print("2. Cadastrar equipe")
    print("3. Adicionar jogador a uma equipe")
    print("4. Listar todas as equipes")
    print("5. Listar jogadores de uma equipe")
    print("6. Buscar jogador por nickname")
    print("7. Remover jogador de uma equipe")
    print("0. Sair")
    print("=" * 40)

option = -1
while True:
    print_menu()
    try:
        option = int(input("Escolha uma opção: "))
    except ValueError:
        print("Opção inválida! Por favor, digite um número.")
        continue
    match option:
        case 0:
            break
        case 1:
            register_player()
        case 2:
            register_team()
        case 3:
            add_player_team()
        case 4:
            print_teams()
        case 5:
            print_players_team()
        case 6:
            search_player()
        case 7:
            remove_player_team()
        case _:
            print("Opção inválida! Por favor, escolha uma opção do menu.")
        