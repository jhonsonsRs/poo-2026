import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from ui import crt_begin, draw_crt, Button, Title, get_background
import audio


class MenuView(arcade.View):
    def __init__(self, window=None):
        super().__init__(window)
        audio.tocar_musica('menu')
        self.bg = get_background()
        cx = SCREEN_WIDTH / 2

        self.titulo = Title(SCREEN_TITLE, cx, SCREEN_HEIGHT - 150, size=72)

        # (texto, atalho, tipo, ação)
        defs = [
            ('Jogar', 'J', 'success', self.ir_jogar),
            ('Instruções', 'I', 'primary', self.ir_instrucoes),
            ('Sobre o Jogo', 'S', 'primary', self.ir_sobre),
            ('Tela de Ranking', 'R', 'primary', self.ir_ranking),
            ('Sair', 'ESC', 'danger', arcade.exit),
        ]
        self.botoes = []
        self.acoes = []
        y = 412
        for texto, atalho, tipo, acao in defs:
            self.botoes.append(
                Button(texto, cx, y, w=380, h=56, hint=atalho, kind=tipo))
            self.acoes.append(acao)
            y -= 66

        self.sel = 0
        self.botoes[0].active = True

    # ---------------------------------------------------------- navegação
    def ir_jogar(self):
        audio.sfx('selecionar')
        from name_view import NameView
        self.window.show_view(NameView())

    def ir_instrucoes(self):
        audio.sfx('selecionar')
        from instructions_view import InstructionsView
        self.window.show_view(InstructionsView())

    def ir_sobre(self):
        audio.sfx('selecionar')
        from about_view import AboutView
        self.window.show_view(AboutView())

    def ir_ranking(self):
        audio.sfx('selecionar')
        from ranking_view import TelaRanking
        self.window.show_view(TelaRanking())

    def _selecionar(self, i):
        if i != self.sel:
            audio.sfx('navegar')
        self.sel = i
        for n, b in enumerate(self.botoes):
            b.active = (n == i)

    # ----------------------------------------------------------- eventos
    def on_update(self, delta_time):
        self.bg.update(delta_time)

    def on_draw(self):
        crt_begin(self.window)
        self.clear()
        self.bg.draw()
        self.titulo.draw()
        for b in self.botoes:
            b.draw()
        draw_crt()

    def on_mouse_motion(self, x, y, dx, dy):
        for i, b in enumerate(self.botoes):
            if b.contains(x, y):
                self._selecionar(i)
                break

    def on_mouse_press(self, x, y, button, modifiers):
        for i, b in enumerate(self.botoes):
            if b.contains(x, y):
                self.acoes[i]()
                return

    def on_key_press(self, key, modifiers):
        if key == arcade.key.J:
            self.ir_jogar()
        elif key == arcade.key.I:
            self.ir_instrucoes()
        elif key == arcade.key.S:
            self.ir_sobre()
        elif key == arcade.key.R:
            self.ir_ranking()
        elif key == arcade.key.ESCAPE:
            arcade.exit()
        elif key == arcade.key.UP:
            self._selecionar((self.sel - 1) % len(self.botoes))
        elif key == arcade.key.DOWN:
            self._selecionar((self.sel + 1) % len(self.botoes))
        elif key in (arcade.key.ENTER, arcade.key.NUM_ENTER):
            self.acoes[self.sel]()
