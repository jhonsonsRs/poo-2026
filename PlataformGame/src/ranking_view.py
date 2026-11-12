import arcade

import audio
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from pontuacao import Pontuacao
from ui import (
    BRONZE, CREAM_DK, FONT, GOLD, INK, Layer, MUTED, SILVER, Title,
    Footer, crt_begin, draw_crt, get_background, rounded_image, circle_image,
)

MAX_LINHAS = 5
PODIO = [GOLD, SILVER, BRONZE]
COLUNAS = (
    ('quick', 'PARTIDA RÁPIDA', 350),
    ('hardcore', 'PARTIDA HARDCORE', 930),
)
Y_CABECALHO = 505
Y_PRIMEIRA = 460
ESPACO_LINHAS = 62


class TelaRanking(arcade.View):
    def __init__(self, window=None):
        super().__init__(window)
        audio.tocar_musica('menu')
        self.bg = get_background()
        self.rankings = {
            modo: list(
                Pontuacao.select()
                .where(Pontuacao.modo == modo)
                .order_by(Pontuacao.pontos.desc())
                .limit(MAX_LINHAS)
            )
            for modo, _, _ in COLUNAS
        }

        cx = SCREEN_WIDTH / 2
        self.titulo = Title('RANKING', cx, SCREEN_HEIGHT - 60, size=40)
        self.rodape = Footer([('M', 'Menu Principal'), ('ESC', 'Sair')])
        self.layer = Layer()
        self.layer.panel(cx, 335, 1160, 500)

        for modo, titulo, coluna_x in COLUNAS:
            self.layer.text(titulo, coluna_x, 560, 20, INK, bold=True)
            self.layer.text('JOGADOR', coluna_x - 190, Y_CABECALHO,
                            11, MUTED, bold=True, ax='left')
            self.layer.text('PONTOS', coluna_x + 100, Y_CABECALHO,
                            11, MUTED, bold=True, ax='right')
            self.layer.text('TEMPO', coluna_x + 190, Y_CABECALHO,
                            11, MUTED, bold=True, ax='right')
            self._faixas(modo, coluna_x)

    def _faixas(self, modo, coluna_x):
        for i in range(len(self.rankings[modo])):
            y = Y_PRIMEIRA - i * ESPACO_LINHAS
            faixa = PODIO[i] if i < 3 else CREAM_DK if i % 2 == 0 else None
            if faixa:
                self.layer.image(rounded_image(500, 50, 6, faixa),
                                 coluna_x, y)
            if i < 3:
                self.layer.image(
                    circle_image(30, (255, 255, 255, 255), ow=3),
                    coluna_x - 225, y
                )

    def on_update(self, delta_time):
        self.bg.update(delta_time)

    def on_draw(self):
        crt_begin(self.window)
        self.clear()
        self.bg.draw()
        self.titulo.draw()
        self.layer.draw()

        for modo, _, coluna_x in COLUNAS:
            registros = self.rankings[modo]
            if not registros:
                arcade.draw_text(
                    'Nenhuma pontuação',
                    coluna_x, 350, INK, 18, font_name=FONT,
                    anchor_x='center', anchor_y='center'
                )
                continue
            for i, registro in enumerate(registros):
                y = Y_PRIMEIRA - i * ESPACO_LINHAS
                arcade.draw_text(
                    str(i + 1) if i < 3 else f'{i + 1}º',
                    coluna_x - 225, y, INK if i < 3 else MUTED, 15,
                    font_name=FONT, bold=i < 3,
                    anchor_x='center', anchor_y='center'
                )
                arcade.draw_text(
                    registro.nome_jogador, coluna_x - 190, y, INK, 16,
                    font_name=FONT, bold=i < 3,
                    anchor_x='left', anchor_y='center'
                )
                arcade.draw_text(
                    str(registro.pontos), coluna_x + 100, y, INK, 16,
                    font_name=FONT, anchor_x='right', anchor_y='center'
                )
                arcade.draw_text(
                    f'{registro.tempo_partida:.1f}s', coluna_x + 190, y,
                    INK, 16, font_name=FONT, anchor_x='right',
                    anchor_y='center'
                )

        self.rodape.draw()
        draw_crt()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.M:
            from menu_view import MenuView
            self.window.show_view(MenuView())
        elif key == arcade.key.ESCAPE:
            arcade.exit()
