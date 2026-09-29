import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from pontuacao import Pontuacao

MAX_LINHAS = 10


class RankingView(arcade.View):
    def __init__(self, window=None):
        super().__init__(window)
        # Consulta uma vez só (não no on_draw, que roda todo frame)
        registros = []
        for reg in Pontuacao.select():
            taxa = reg.pontuacao / reg.tempo if reg.tempo > 0 else 0
            registros.append((reg, taxa))

        # Maior moedas/segundo primeiro; empate decide por mais moedas
        registros.sort(key=lambda r: (r[1], r[0].pontuacao), reverse=True)
        self.registros = registros[:MAX_LINHAS]

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            'RANKING',
            SCREEN_WIDTH / 2, SCREEN_HEIGHT - 70,
            arcade.color.GOLD, font_size=40,
            anchor_x='center', bold=True
        )

        if not self.registros:
            arcade.draw_text(
                'Nenhuma pontuação registrada ainda.',
                SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                arcade.color.LIGHT_GRAY, font_size=20,
                anchor_x='center'
            )
        else:
            x_pos = SCREEN_WIDTH / 2 - 320
            x_nome = SCREEN_WIDTH / 2 - 250
            x_moedas = SCREEN_WIDTH / 2 + 60
            x_tempo = SCREEN_WIDTH / 2 + 180
            x_taxa = SCREEN_WIDTH / 2 + 310

            # Cabeçalho
            y_cab = SCREEN_HEIGHT - 125
            cinza = arcade.color.LIGHT_GRAY
            arcade.draw_text('#', x_pos, y_cab, cinza, font_size=16,
                             anchor_x='left')
            arcade.draw_text('Jogador', x_nome, y_cab, cinza, font_size=16,
                             anchor_x='left')
            arcade.draw_text('Moedas', x_moedas, y_cab, cinza, font_size=16,
                             anchor_x='right')
            arcade.draw_text('Tempo', x_tempo, y_cab, cinza, font_size=16,
                             anchor_x='right')
            arcade.draw_text('Moedas/s', x_taxa, y_cab, cinza, font_size=16,
                             anchor_x='right')

            cores_podio = [
                arcade.color.GOLD,
                arcade.color.SILVER,
                arcade.color.BRONZE,
            ]
            for i, (reg, taxa) in enumerate(self.registros):
                y = SCREEN_HEIGHT - 165 - i * 35
                cor = cores_podio[i] if i < 3 else arcade.color.WHITE

                arcade.draw_text(f'{i + 1}º', x_pos, y, cor, font_size=20,
                                 anchor_x='left', bold=True)
                arcade.draw_text(reg.nome_player, x_nome, y, cor,
                                 font_size=20, anchor_x='left')
                arcade.draw_text(f'{reg.pontuacao:g}', x_moedas, y, cor,
                                 font_size=20, anchor_x='right')
                arcade.draw_text(f'{reg.tempo:.1f}s', x_tempo, y, cor,
                                 font_size=20, anchor_x='right')
                arcade.draw_text(f'{taxa:.2f}', x_taxa, y, cor,
                                 font_size=20, anchor_x='right', bold=True)

        arcade.draw_text(
            '[M] Menu Principal   [ESC] Sair',
            SCREEN_WIDTH / 2, 50,
            arcade.color.LIGHT_GRAY, font_size=18,
            anchor_x='center'
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.M:
            from menu_view import MenuView
            self.window.show_view(MenuView())
        elif key == arcade.key.ESCAPE:
            arcade.exit()