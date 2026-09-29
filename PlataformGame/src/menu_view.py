import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE


class MenuView(arcade.View):
    def __init__(self, window=None):
        super().__init__(window)

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            SCREEN_TITLE,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 150,
            arcade.color.WHITE,
            font_size=48,
            anchor_x='center',
            bold=True
        )

        opcoes = [
            '[J] Jogar',
            '[I] Instruções',
            '[S] Sobre o Jogo',
            '[R] Tela de Ranking',  
            '[ESC] Sair',
        ]
        for i, texto in enumerate(opcoes):
            arcade.draw_text(
                texto,
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2 + 40 - i * 45,
                arcade.color.LIGHT_GRAY,
                font_size=22,
                anchor_x='center',
            )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.J:
            from name_view import NameView
            self.window.show_view(NameView())

        elif key == arcade.key.I:
            from instructions_view import InstructionsView
            self.window.show_view(InstructionsView())

        elif key == arcade.key.S:
            from about_view import AboutView
            self.window.show_view(AboutView())

        elif key == arcade.key.R:
            from ranking_view import RankingView
            self.window.show_view(RankingView())

        elif key == arcade.key.ESCAPE:
            arcade.exit()