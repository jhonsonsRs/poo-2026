import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from ui import (Layer, Title, Footer, Button, T, get_background,
                rounded_image, make_sprite, INK, MUTED, RED)

MAX_NOME = 16


class NameView(arcade.View):

    def __init__(self, window=None):
        super().__init__(window)
        self.bg = get_background()
        self.nome = ''
        self.erro = ''
        self.tempo = 0.0

        cx = SCREEN_WIDTH / 2
        self.campo_w = 480
        self.campo_h = 60
        self.campo_x = cx
        self.campo_y = 385

        self.btn_w = 260
        self.btn_h = 56
        self.btn_x = cx
        self.btn_y = 265

        self.titulo = Title('Digite seu nome', cx, SCREEN_HEIGHT - 130,
                            size=38)
        self.rodape = Footer([('ENTER', 'Confirmar'), ('ESC', 'Voltar')])

        L = self.layer = Layer()
        L.panel(cx, 335, 700, 270)

        # campo de texto com brilho dourado (sempre em foco)
        img = rounded_image(self.campo_w, self.campo_h, 14,
                            (255, 255, 255, 255), outline=INK, ow=3)
        L.image(img, self.campo_x, self.campo_y)

        self.botao = Button('PRONTO', self.btn_x, self.btn_y,
                            w=self.btn_w, h=self.btn_h, kind='success',
                            size=22)

        esq = self.campo_x - self.campo_w / 2
        dir_ = self.campo_x + self.campo_w / 2
        self.texto = T('|', esq + 18, self.campo_y, 24, INK,
                       ax='left')
        self.contador = T(f'0/{MAX_NOME}', dir_, self.campo_y - 50, 13,
                          MUTED, ax='right')
        self.msg_erro = T('', esq, self.campo_y - 50, 14, RED, ax='left')

    # ----------------------------------------------------------- eventos
    def on_update(self, delta_time):
        self.tempo += delta_time
        self.bg.update(delta_time)

    def on_mouse_motion(self, x, y, dx, dy):
        self.botao.active = self.botao.contains(x, y)

    def on_draw(self):
        self.clear()
        self.bg.draw()
        self.titulo.draw()
        self.layer.draw()

        cursor = '|' if int(self.tempo * 2) % 2 == 0 else ' '
        self.texto.text = self.nome + cursor
        self.texto.draw()

        self.contador.text = f'{len(self.nome)}/{MAX_NOME}'
        self.contador.draw()
        if self.erro:
            self.msg_erro.text = self.erro
            self.msg_erro.draw()

        self.botao.draw()
        self.rodape.draw()

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
        if self.botao.contains(x, y):
            self.confirmar()

    def confirmar(self):
        nome = self.nome.strip()

        if not nome:
            self.erro = 'Digite um nome antes de continuar.'
            return
        from game_view import GameView
        self.window.show_view(GameView(nome))
