import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from pontuacao import Pontuacao
from ui import (draw_crt, Layer, Title, Footer, get_background, rounded_image,
                circle_image, GOLD, SILVER, BRONZE, INK, MUTED, CREAM_DK)

MAX_LINHAS = 10

X_POS = 215
X_NOME = 275
X_MOEDAS = 710
X_TEMPO = 850
X_TAXA = 1065

PODIO = [GOLD, SILVER, BRONZE]


class RankingView(arcade.View):
    def __init__(self, window=None):
        super().__init__(window)
        self.bg = get_background()

        # Consulta uma vez só (não no on_draw, que roda todo frame)
        registros = []
        for reg in Pontuacao.select():
            taxa = reg.pontuacao / reg.tempo if reg.tempo > 0 else 0
            registros.append((reg, taxa))

        # Maior moedas/segundo primeiro; empate decide por mais moedas
        registros.sort(key=lambda r: (r[1], r[0].pontuacao), reverse=True)
        self.registros = registros[:MAX_LINHAS]

        cx = SCREEN_WIDTH / 2
        self.titulo = Title('RANKING', cx, SCREEN_HEIGHT - 60, size=40)
        self.rodape = Footer([('M', 'Menu Principal'), ('ESC', 'Sair')])

        L = self.layer = Layer()
        L.panel(cx, 352, 1000, 490)

        if not self.registros:
            L.text('Nenhuma pontuação registrada ainda.', cx, 370, 22, INK)
        else:
            self._tabela(L)

    def _tabela(self, L):
        y_cab = 565
        L.text('JOGADOR', X_NOME, y_cab, 12, MUTED, bold=True, ax='left')
        L.text('MOEDAS', X_MOEDAS, y_cab, 12, MUTED, bold=True, ax='right')
        L.text('TEMPO', X_TEMPO, y_cab, 12, MUTED, bold=True, ax='right')
        L.text('MOEDAS/S', X_TAXA, y_cab, 12, MUTED, bold=True, ax='right')

        for i, (reg, taxa) in enumerate(self.registros):
            y = 520 - i * 41
            podio = i < 3
            cor = INK

            # faixa de fundo (tingida nos 3 primeiros)
            if podio:
                faixa = PODIO[i]
            elif i % 2 == 0:
                faixa = CREAM_DK
            else:
                faixa = None
            if faixa:
                L.image(rounded_image(940, 38, 6, faixa), 640, y)

            # posição: medalha para o pódio, número simples para o resto
            if podio:
                L.image(circle_image(30, (255, 255, 255, 255), ow=3), X_POS, y)
                L.text(str(i + 1), X_POS, y, 15, INK, bold=True)
            else:
                L.text(f'{i + 1}º', X_POS, y, 16, MUTED, bold=True)

            L.text(reg.nome_player, X_NOME, y, 18, cor, bold=podio,
                   ax='left')
            L.text(f'{reg.pontuacao:g}', X_MOEDAS, y, 18, cor, ax='right')
            L.text(f'{reg.tempo:.1f}s', X_TEMPO, y, 18, cor, ax='right')
            L.text(f'{taxa:.2f}', X_TAXA, y, 18, cor, bold=True, ax='right')

    def on_update(self, delta_time):
        self.bg.update(delta_time)

    def on_draw(self):
        self.clear()
        self.bg.draw()
        self.titulo.draw()
        self.layer.draw()
        self.rodape.draw()
        draw_crt()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.M:
            from menu_view import MenuView
            self.window.show_view(MenuView())
        elif key == arcade.key.ESCAPE:
            arcade.exit()
