import math

import arcade
from PIL import Image, ImageDraw


def _checkpoint_image(active: bool):
    image = Image.new('RGBA', (64, 112), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    pole = (74, 52, 48, 255)
    outline = (43, 38, 64, 255)
    flag = (84, 182, 88, 255) if active else (122, 104, 104, 255)
    flag_light = (152, 226, 98, 255) if active else (180, 170, 170, 255)

    draw.rounded_rectangle((28, 8, 36, 104), 4, fill=outline)
    draw.rounded_rectangle((30, 10, 34, 102), 2, fill=pole)
    draw.polygon(
        ((34, 12), (58, 24), (34, 40)),
        fill=outline,
    )
    draw.polygon(
        ((36, 16), (54, 25), (36, 34)),
        fill=flag,
    )
    draw.line((38, 19, 51, 25), fill=flag_light, width=3)
    draw.ellipse((22, 98, 42, 110), fill=outline)
    draw.ellipse((25, 99, 39, 107), fill=(214, 98, 48, 255))
    return image


class Checkpoint(arcade.Sprite):
    def __init__(self, x: float, y: float):
        super().__init__(arcade.Texture(_checkpoint_image(False)), 1.0)
        self.center_x = x
        self.center_y = y
        self.active = False
        self._pulse = 0.0
        self._activated_timer = 0.0

    def activate(self):
        if self.active:
            return False
        self.active = True
        self.texture = arcade.Texture(_checkpoint_image(True))
        self._activated_timer = 0.8
        return True

    def update(self, delta_time: float = 1 / 60):
        self._pulse += delta_time
        if self._activated_timer > 0:
            self._activated_timer = max(0, self._activated_timer - delta_time)
            self.angle = math.sin(self._pulse * 12) * 3
        else:
            self.angle = math.sin(self._pulse * 2) * 1.5
