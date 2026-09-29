import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

MAX_NOME = 16


class NameView(arcade.View):
 
    def __init__(self, window=None):
        super().__init__(window)
        self.nome = ''
        self.erro = ''
        self.tempo = 0.0

        self.campo_w = 400
        self.campo_h = 50
        self.campo_x = SCREEN_WIDTH / 2
        self.campo_y = SCREEN_HEIGHT / 2

        self.btn_w = 200
        self.btn_h = 50
        self.btn_x = SCREEN_WIDTH / 2
        self.btn_y = SCREEN_HEIGHT / 2 - 110

    def on_update(self, delta_time):
        self.tempo += delta_time

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            'Digite seu nome',
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 120,
            arcade.color.WHITE, font_size=36,
            anchor_x='center', bold=True
        )

        esq = self.campo_x - self.campo_w / 2
        dir_ = self.campo_x + self.campo_w / 2
        baixo = self.campo_y - self.campo_h / 2
        cima = self.campo_y + self.campo_h / 2
        arcade.draw_lrbt_rectangle_outline(
            esq, dir_, baixo, cima, arcade.color.WHITE, 2
        )

        cursor = '|' if int(self.tempo * 2) % 2 == 0 else ' '
        arcade.draw_text(
            self.nome + cursor,
            esq + 12, self.campo_y,
            arcade.color.WHITE, font_size=22,
            anchor_x='left', anchor_y='center'
        )

        if self.erro:
            arcade.draw_text(
                self.erro,
                SCREEN_WIDTH / 2, self.campo_y - 50,
                arcade.color.RED, font_size=16,
                anchor_x='center'
            )

        arcade.draw_lrbt_rectangle_filled(
            self.btn_x - self.btn_w / 2, self.btn_x + self.btn_w / 2,
            self.btn_y - self.btn_h / 2, self.btn_y + self.btn_h / 2,
            arcade.color.DARK_GREEN
        )
        arcade.draw_text(
            'PRONTO',
            self.btn_x, self.btn_y,
            arcade.color.WHITE, font_size=22,
            anchor_x='center', anchor_y='center', bold=True
        )

        arcade.draw_text(
            '[ENTER] Confirmar   [ESC] Voltar',
            SCREEN_WIDTH / 2, 80,
            arcade.color.LIGHT_GRAY, font_size=18,
            anchor_x='center'
        )

    def on_text(self, text):
        if len(self.nome) >= MAX_NOME:
            return
        if text.isprintable():
            self.nome += text
            self.erro = ''

    def on_key_press(self, key, modifiers):
        if key == arcade.key.BACKSPACE:
            self.nome = self.nome[:-1]
        elif key in (arcade.key.ENTER, arcade.key.NUM_ENTER):
            self.confirmar()
        elif key == arcade.key.ESCAPE:
            from menu_view import MenuView
            self.window.show_view(MenuView())

    def on_mouse_press(self, x, y, button, modifiers):
        if (abs(x - self.btn_x) <= self.btn_w / 2
                and abs(y - self.btn_y) <= self.btn_h / 2):
            self.confirmar()

    def confirmar(self):
        nome = self.nome.strip()
        
        if not nome:
            self.erro = 'Digite um nome antes de continuar.'
            return
        from game_view import GameView
        self.window.show_view(GameView(nome))