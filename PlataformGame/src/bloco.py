import arcade
from constants import TILE_SIZE, TILEMAP_SCALE


class Bloco(arcade.Sprite):
    """Bloco sólido do cenário (chão e plataformas).

    Todos os Blocos ficam numa arcade.SpriteList que serve de `walls`
    para o PhysicsEnginePlatformer.
    """

    LADO = TILE_SIZE * TILEMAP_SCALE

    def __init__(self, textura: arcade.Texture, x: float, y: float,
                 escala: float = TILEMAP_SCALE):
        super().__init__(textura, escala)
        self.center_x = x
        self.center_y = y

    @classmethod
    def de_tile(cls, tile: arcade.Sprite) -> "Bloco":
        """Converte um tile da camada de plataformas do Tiled em Bloco."""
        return cls(tile.texture, tile.center_x, tile.center_y)

    @classmethod
    def plataforma(cls, textura: arcade.Texture, x: float, y: float,
                   quantidade: int) -> list["Bloco"]:
        """Cria uma fileira horizontal de blocos começando em (x, y)."""
        return [cls(textura, x + i * cls.LADO, y) for i in range(quantidade)]
