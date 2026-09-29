import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from pontuacao import Pontuacao


class GameOverView(arcade.View):
    def __init__(self, score: int, max_score: int, tempo: float, nome: str, window=None):
        super().__init__(window)
        self.score = score
        self.max_score = max_score
        self.tempo = tempo
        self.nome = nome
        self.vitoria_perfeita = score >= max_score

        Pontuacao.create(nome_player=nome, pontuacao=score)

    def on_draw(self):
        self.clear()

        if self.vitoria_perfeita:
            titulo = 'PARABÉNS! VITÓRIA PERFEITA!'
            cor_titulo = arcade.color.GOLD
            mensagem = 'Você escapou de todos os inimigos perfeitamente!'
        else:
            titulo = 'Parabéns!'
            cor_titulo = arcade.color.WHITE
            mensagem = 'Você coletou todas as moedas!'

        arcade.draw_text(
            titulo,
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 150,
            cor_titulo, font_size=36,
            anchor_x='center', bold=True
        )
        arcade.draw_text(
            mensagem,
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 90,
            arcade.color.LIGHT_GRAY, font_size=20,
            anchor_x='center',
        )
        arcade.draw_text(
            f'Jogador: {self.nome}',
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40,
            arcade.color.WHITE, font_size=24,
            anchor_x='center', bold=True
        )
        arcade.draw_text(
            f'Pontuação final: {self.score}',
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 10,
            arcade.color.WHITE, font_size=24,
            anchor_x='center', bold=True
        )
        arcade.draw_text(
            f'Tempo total: {self.tempo:.1f}s',
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60,
            arcade.color.LIGHT_GRAY, font_size=20,
            anchor_x='center',
        )
        arcade.draw_text(
            '[M] Menu Principal   [ESC] Sair',
            SCREEN_WIDTH / 2, 80,
            arcade.color.LIGHT_GRAY, font_size=18,
            anchor_x='center',
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.M:
            from menu_view import MenuView
            self.window.show_view(MenuView())
        elif key == arcade.key.ESCAPE:
            arcade.exit()