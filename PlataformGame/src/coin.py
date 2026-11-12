import random
import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

FLY_SHEET = '../sprites/Fly_tiles.png'
FLY_FRAMES = 6

# Cache: o sheet é fatiado uma única vez e reaproveitado por todas as moscas
_cache = None


def _load_fly_textures():
    """Retorna (texturas_direita, texturas_esquerda)."""
    global _cache
    if _cache is None:
        sheet = arcade.texture.spritesheet.SpriteSheet(FLY_SHEET)
        direita = []
        for i in range(FLY_FRAMES):
            rect = arcade.LRBT(i * 16, i * 16 + 16, 0, 16)
            direita.append(sheet.get_texture(rect))
        esquerda = [t.flip_left_right() for t in direita]
        _cache = (direita, esquerda)
    return _cache


class Coin(arcade.Sprite):
    """Mosca coletável. (O nome Coin foi mantido para não mudar o resto do jogo.)

    O parâmetro `sprite` é mantido só por compatibilidade com o GameView:
    as moscas sempre usam o Fly_tiles.png.
    """

    def __init__(self, sprite: str, scale: float, value: int,
                 facing_right: bool | None = None):
        super().__init__()
        self.scale = scale
        self.value = value
        self.FRAME_SPEED = 0.06

        self._right, self._left = _load_fly_textures()
        if facing_right is None:
            facing_right = random.choice((True, False))
        self.facing_right = facing_right
        self.textures_list = self._right if facing_right else self._left

        # cada mosca começa num ponto diferente da batida de asas
        self.current_frame = random.randrange(FLY_FRAMES)
        self.frame_timer = random.uniform(0, self.FRAME_SPEED)
        self.texture = self.textures_list[self.current_frame]

    def _set_facing(self, right: bool):
        if right != self.facing_right:
            self.facing_right = right
            self.textures_list = self._right if right else self._left
            self.texture = self.textures_list[self.current_frame]

    def _animate(self, delta_time: float):
        self.frame_timer += delta_time
        if self.frame_timer >= self.FRAME_SPEED:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.textures_list)
            self.texture = self.textures_list[self.current_frame]

    def update(self, delta_time: float = 1/60):
        self._animate(delta_time)


class SpecialCoin(Coin):
    """Mosca especial: voa pela tela quicando e olha para onde está indo."""

    def __init__(self, scale: float):
        super().__init__(FLY_SHEET, scale, value=5)
        self.change_x = random.choice([-3, 3])
        self.change_y = random.choice([-3, 3])
        self.world_width = SCREEN_WIDTH
        self.world_height = SCREEN_HEIGHT
        self._set_facing(self.change_x > 0)

    def update(self, delta_time: float = 1/60):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left <= 0 or self.right >= self.world_width:
            self.change_x *= -1
        if self.bottom <= 0 or self.top >= self.world_height:
            self.change_y *= -1

        self._set_facing(self.change_x > 0)
        self._animate(delta_time)