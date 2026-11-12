import math

import arcade


_BOSS_PROJECTILE_TEXTURE = arcade.load_texture(
    '../sprites/Boss/boss_projectile.png'
)


class EnemyProjectile(arcade.SpriteSolidColor):
    def __init__(self, x: float, y: float, target_x: float, target_y: float):
        super().__init__(14, 14, arcade.color.MAGENTA)
        self.texture = _BOSS_PROJECTILE_TEXTURE
        self.center_x = x
        self.center_y = y
        distance = math.hypot(target_x - x, target_y - y) or 1.0
        self.change_x = (target_x - x) / distance * 6.0
        self.change_y = (target_y - y) / distance * 6.0
        self.angle = math.degrees(math.atan2(self.change_y, self.change_x))
        self.damage = 1
