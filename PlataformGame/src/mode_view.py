import arcade

import audio
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from ui import (
    crt_begin, draw_crt, Button, Footer, Layer, MUTED, Title, get_background,
)


class ModeView(arcade.View):
    def __init__(self, player_name: str, window=None):
        super().__init__(window)
        audio.tocar_musica('menu')
        self.player_name = player_name
        self.bg = get_background()
        self.selected = 0

        cx = SCREEN_WIDTH / 2
        self.title = Title('Escolha o modo de jogo', cx, SCREEN_HEIGHT - 130,
                           size=38)
        self.layer = Layer()
        self.layer.panel(cx, 360, 820, 390)
        self.layer.text(
            f'Jogador: {player_name}', cx, 480, 18, MUTED, bold=True
        )
        self.layer.text(
            'Os dois modos usam as regras atuais por enquanto.',
            cx, 445, 15, MUTED
        )
        self.layer.text(
            'As próximas novidades serão exclusivas do Hardcore.',
            cx, 418, 15, MUTED
        )

        self.buttons = [
            Button(
                'Partida Rápida', cx, 340, w=480, h=60,
                hint='R', kind='success', size=21
            ),
            Button(
                'Partida Hardcore', cx, 255, w=480, h=60,
                hint='H', kind='danger', size=21
            ),
        ]
        self.footer = Footer([('ESC', 'Voltar')])
        self._select(0)

    def _select(self, index: int):
        self.selected = index
        for i, button in enumerate(self.buttons):
            button.active = i == index

    def _start(self, mode: str):
        audio.sfx('selecionar')
        from game_view import GameView
        self.window.show_view(
            GameView(self.player_name, game_mode=mode)
        )

    def on_update(self, delta_time):
        self.bg.update(delta_time)

    def on_draw(self):
        crt_begin(self.window)
        self.clear()
        self.bg.draw()
        self.layer.draw()
        self.title.draw()
        for button in self.buttons:
            button.draw()
        self.footer.draw()
        draw_crt()

    def on_mouse_motion(self, x, y, dx, dy):
        for i, button in enumerate(self.buttons):
            if button.contains(x, y):
                self._select(i)
                return

    def on_mouse_press(self, x, y, button, modifiers):
        for i, mode_button in enumerate(self.buttons):
            if mode_button.contains(x, y):
                self._select(i)
                self._start('quick' if i == 0 else 'hardcore')
                return

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            self._start('quick')
        elif key == arcade.key.H:
            self._start('hardcore')
        elif key == arcade.key.ESCAPE:
            from name_view import NameView
            self.window.show_view(NameView())
        elif key == arcade.key.UP:
            self._select((self.selected - 1) % len(self.buttons))
        elif key == arcade.key.DOWN:
            self._select((self.selected + 1) % len(self.buttons))
        elif key in (arcade.key.ENTER, arcade.key.NUM_ENTER):
            self._start('quick' if self.selected == 0 else 'hardcore')
