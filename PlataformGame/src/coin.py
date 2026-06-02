import arcade

class Coin(arcade.Sprite):
    def __init__(self, sprite : str, scale: float, value: int):
        super().__init__(sprite, scale)
        self.value = value