import math
import random

import arcade


class EffectParticle(arcade.SpriteSolidColor):
    def __init__(
        self,
        x: float,
        y: float,
        color: tuple[int, int, int],
        size: float,
        velocity_x: float,
        velocity_y: float,
        lifetime: float,
        gravity: float = 0.0,
    ):
        super().__init__(max(1, int(size)), max(1, int(size)), color)
        self.center_x = x
        self.center_y = y
        self.change_x = velocity_x
        self.change_y = velocity_y
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.gravity = gravity

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.change_y -= self.gravity * delta_time
        self.lifetime -= delta_time
        self.alpha = max(
            0, int(255 * max(0.0, self.lifetime / self.max_lifetime))
        )


def create_burst(
    particles: arcade.SpriteList,
    x: float,
    y: float,
    color: tuple[int, int, int],
    count: int = 8,
    speed: float = 3.0,
    size: float = 4.0,
    lifetime: float = 0.45,
    gravity: float = 0.08,
):
    for _ in range(count):
        angle = random.uniform(0, math.tau)
        velocity = random.uniform(speed * 0.45, speed)
        particles.append(
            EffectParticle(
                x, y, color, size,
                math.cos(angle) * velocity,
                math.sin(angle) * velocity,
                random.uniform(lifetime * 0.7, lifetime),
                gravity,
            )
        )
