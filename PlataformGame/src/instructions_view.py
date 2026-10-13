import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from ui import (crt_begin, draw_crt, Layer, Title, Footer, get_background, rounded_image,
                circle_image, INK, MUTED, ORANGE)

COL_ESQ = 140
COL_DIR = 700


class InstructionsView(arcade.View):
    def __init__(self, window=None):
        super().__init__(window)
        self.bg = get_background()
        cx = SCREEN_WIDTH / 2
        self.titulo = Title('Instruções', cx, SCREEN_HEIGHT - 60, size=38)
        self.rodape = Footer([('M', 'Voltar ao Menu'), ('ESC', 'Voltar')])

        L = self.layer = Layer()
        L.panel(cx, 370, 1100, 450)
        # divisória entre as colunas
        L.image(rounded_image(4, 350, 2, (43, 38, 64, 40)), cx + 10, 370)

        self._coluna_esquerda(L)
        self._coluna_direita(L)

    # ------------------------------------------------------------ blocos
    def _cabecalho(self, L, texto, x, y):
        L.text(texto, x, y, 14, ORANGE, bold=True, ax='left')

    def _coluna_esquerda(self, L):
        x = COL_ESQ
        self._cabecalho(L, 'OBJETIVO', x, 555)
        L.text('Colete todas as moedas para vencer!', x, 520, 18,
               INK, ax='left')
        L.text('Desvie dos inimigos: cada colisão custa pontos.', x, 490,
               15, MUTED, ax='left')

        self._cabecalho(L, 'CONTROLES', x, 430)
        y = 380
        # A + seta esquerda
        L.keycap('A', x + 22, y)
        L.keycap('', x + 74, y, w=44, symbol='left')
        L.text('Mover para a esquerda', x + 140, y, 17, INK, ax='left')
        y -= 62
        L.keycap('D', x + 22, y)
        L.keycap('', x + 74, y, w=44, symbol='right')
        L.text('Mover para a direita', x + 140, y, 17, INK, ax='left')
        y -= 62
        L.keycap('SPACE', x + 48, y, w=96)
        L.text('Pular', x + 140, y, 17, INK, ax='left')

    def _coluna_direita(self, L):
        x = COL_DIR
        self._cabecalho(L, 'INIMIGOS', x, 555)

        y = 515
        self._inimigo(L, x, y, (232, 84, 98), 'Inimigo comum',
                      ['Patrulha o mapa.',
                       'Cada colisão remove 1 ponto.'])
        y -= 88
        self._inimigo(L, x, y, (255, 132, 200), 'Inimigo especial',
                      ['Persegue você pelo mapa.',
                       'Teleporta ao colidir e remove 1 ponto.'])

        self._cabecalho(L, 'MOEDAS', x, 325)
        y = 280
        self._moeda(L, x, y, '1', (255, 196, 61), (196, 134, 20),
                    'Moeda comum', 'Vale 1 ponto.')
        y -= 66
        self._moeda(L, x, y, '5', (255, 226, 120), (176, 100, 255),
                    'Moeda especial', 'Quica nas bordas e vale 5 pontos.')

    def _inimigo(self, L, x, y, cor, titulo, linhas):
        L.image(circle_image(22, cor + (255,), ow=3), x + 12, y)
        L.text(titulo, x + 38, y, 17, INK, bold=True, ax='left')
        for i, linha in enumerate(linhas):
            L.text(linha, x + 38, y - 28 - i * 24, 15, MUTED, ax='left')

    def _moeda(self, L, x, y, valor, cor, borda, titulo, desc):
        L.image(circle_image(40, cor + (255,), ow=4),
                x + 20, y - 12)
        L.text(valor, x + 20, y - 12, 16, INK, bold=True)
        L.text(titulo, x + 52, y, 17, INK, bold=True, ax='left')
        L.text(desc, x + 52, y - 26, 15, MUTED, ax='left')

    # ----------------------------------------------------------- eventos
    def on_update(self, delta_time):
        self.bg.update(delta_time)

    def on_draw(self):
        crt_begin(self.window)
        self.clear()
        self.bg.draw()
        self.titulo.draw()
        self.layer.draw()
        self.rodape.draw()
        draw_crt()

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.ESCAPE, arcade.key.M):
            from menu_view import MenuView
            self.window.show_view(MenuView())
