import arcade
import math


class Projectile(arcade.SpriteSolidColor):
    """Projétil simples disparado horizontalmente pelo jogador."""

    def __init__(self, x: float, y: float, target_x: float, target_y: float):
        super().__init__(14, 6, arcade.color.YELLOW_ORANGE)
        self.center_x = x
        self.center_y = y
        distance = math.hypot(target_x - x, target_y - y) or 1.0
        self.change_x = (target_x - x) / distance * 12.0
        self.change_y = (target_y - y) / distance * 12.0
        self.angle = math.degrees(math.atan2(self.change_y, self.change_x))

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x
        self.center_y += self.change_y
