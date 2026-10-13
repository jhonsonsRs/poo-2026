import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from pontuacao import Pontuacao
from ui import (draw_crt, Layer, Title, Button, get_background, rounded_image,
                GOLD, MUTED, WHITE, INK, ORANGE, CREAM_DK)


class GameOverView(arcade.View):
    def __init__(self, score: int, max_score: int, tempo: float, nome: str, window=None):
        super().__init__(window)
        self.bg = get_background()
        self.score = score
        self.max_score = max_score
        self.tempo = tempo
        self.nome = nome
        self.vitoria_perfeita = score >= max_score

        Pontuacao.create(nome_player=nome, pontuacao=score, tempo=tempo)

        cx = SCREEN_WIDTH / 2
        if self.vitoria_perfeita:
            titulo = 'PARABÉNS! VITÓRIA PERFEITA!'
            cor_titulo = GOLD
            mensagem = 'Você escapou de todos os inimigos perfeitamente!'
        else:
            titulo = 'Parabéns!'
            cor_titulo = WHITE
            mensagem = 'Você coletou todas as moedas!'

        L = self.layer = Layer()
        L.panel(cx, 382, 1140, 450)
        self.titulo = Title(titulo, cx, 548, size=36, color=cor_titulo)
        L.text(mensagem, cx, 462, 19, MUTED)

        # três cartões de estatística
        card_w, card_h, gap = 330, 130, 24
        xs = [cx - card_w - gap, cx, cx + card_w + gap]
        destaque = ORANGE if self.vitoria_perfeita else WHITE
        tam_nome = 30 if len(nome) <= 9 else 24 if len(nome) <= 13 else 20
        cards = [
            ('JOGADOR', nome, tam_nome, INK),
            ('PONTUAÇÃO FINAL', f'{score:g}', 40, destaque),
            ('TEMPO TOTAL', f'{tempo:.1f}s', 40, INK),
        ]
        card_img = rounded_image(card_w, card_h, 12, CREAM_DK,
                                 outline=INK, ow=3)
        for x, (rotulo, valor, tam, cor) in zip(xs, cards):
            L.image(card_img, x, 360)
            L.text(rotulo, x, 403, 12, MUTED, bold=True)
            L.text(valor, x, 351, tam, cor, bold=True)

        self.botoes = [
            Button('Menu Principal', cx - 190, 225, w=340, h=56,
                   hint='M', kind='primary'),
            Button('Sair', cx + 190, 225, w=340, h=56,
                   hint='ESC', kind='danger'),
        ]
        self.acoes = [self.ir_menu, arcade.exit]

    def ir_menu(self):
        from menu_view import MenuView
        self.window.show_view(MenuView())

    def on_update(self, delta_time):
        self.bg.update(delta_time)

    def on_mouse_motion(self, x, y, dx, dy):
        for b in self.botoes:
            b.active = b.contains(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        for b, acao in zip(self.botoes, self.acoes):
            if b.contains(x, y):
                acao()
                return

    def on_draw(self):
        self.clear()
        self.bg.draw()
        self.layer.draw()
        self.titulo.draw()
        for b in self.botoes:
            b.draw()
        draw_crt()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.M:
            self.ir_menu()
        elif key == arcade.key.ESCAPE:
            arcade.exit()
