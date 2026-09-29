import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from pontuacao import Pontuacao

MAX_LINHAS = 10


class RankingView(arcade.View):
    def __init__(self, window=None):
        super().__init__(window)
        # Consulta uma vez só (não no on_draw, que roda todo frame)
        self.registros = list(
            Pontuacao.select()
            .order_by(Pontuacao.pontuacao.desc())
            .limit(MAX_LINHAS)
        )

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            'RANKING',
            SCREEN_WIDTH / 2, SCREEN_HEIGHT - 80,
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
            cores_podio = [
                arcade.color.GOLD,
                arcade.color.SILVER,
                arcade.color.BRONZE,
            ]
            for i, reg in enumerate(self.registros):
                y = SCREEN_HEIGHT - 150 - i * 35
                cor = cores_podio[i] if i < 3 else arcade.color.WHITE

                arcade.draw_text(
                    f'{i + 1}º',
                    SCREEN_WIDTH / 2 - 250, y,
                    cor, font_size=20, anchor_x='left', bold=True
                )
                arcade.draw_text(
                    reg.nome_player,
                    SCREEN_WIDTH / 2 - 180, y,
                    cor, font_size=20, anchor_x='left'
                )
                arcade.draw_text(
                    f'{reg.pontuacao:g}',
                    SCREEN_WIDTH / 2 + 250, y,
                    cor, font_size=20, anchor_x='right', bold=True
                )

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