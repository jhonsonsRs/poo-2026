import arcade

ALTURA = 600
LARGURA = 800
TITULO = "Meu Jogo"
VELOCIDADE = 5

class JanelaJogo(arcade.Window):
    def __init__(self):
        super().__init__(LARGURA, ALTURA, TITULO)
        arcade.set_background_color(arcade.color.BLACK)
        self.jogo_rodando = True

        self.x = LARGURA / 2
        self.y = ALTURA / 2

        self.cima = False
        self.baixo = False
        self.esquerda = False
        self.direita = False

        # Carrega as sprites
        self.sprites = {
            "cima":     arcade.load_texture("shizuka_up.png"),
            "baixo":    arcade.load_texture("shizuka_down.png"),
            "esquerda": arcade.load_texture("shizuka_left.png"),
            "direita":  arcade.load_texture("shizuka_right.png"),
        }
        self.direcao_atual = "baixo"

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            self.sprites[self.direcao_atual],
            arcade.XYWH(self.x, self.y, 64, 64)
        )

    def on_update(self, delta_time):
        if self.cima:
            self.y += VELOCIDADE
            self.direcao_atual = "cima"
        if self.baixo:
            self.y -= VELOCIDADE
            self.direcao_atual = "baixo"
        if self.esquerda:
            self.x -= VELOCIDADE
            self.direcao_atual = "esquerda"
        if self.direita:
            self.x += VELOCIDADE
            self.direcao_atual = "direita"

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.cima = True
        if key == arcade.key.S:
            self.baixo = True
        if key == arcade.key.A:
            self.esquerda = True
        if key == arcade.key.D:
            self.direita = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.cima = False
        if key == arcade.key.S:
            self.baixo = False
        if key == arcade.key.A:
            self.esquerda = False
        if key == arcade.key.D:
            self.direita = False

def main():
    jogo = JanelaJogo()
    arcade.run()

if __name__ == "__main__":
    main()