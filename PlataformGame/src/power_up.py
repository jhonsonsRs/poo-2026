import math

import arcade
from PIL import Image, ImageDraw


POWER_UP_COLORS = {
    'health': ((214, 64, 64), (255, 170, 170)),
    'rapid_fire': ((66, 134, 228), (170, 220, 255)),
    'shield': ((84, 182, 88), (190, 255, 170)),
}


def _power_up_image(kind: str):
    base, shine = POWER_UP_COLORS[kind]
    image = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    outline = (43, 38, 64, 255)
    draw.ellipse((4, 8, 60, 64), fill=outline)
    draw.ellipse((9, 5, 55, 55), fill=base + (255,))
    draw.ellipse((15, 11, 38, 28), fill=shine + (220,))

    if kind == 'health':
        draw.rectangle((28, 17, 36, 45), fill=(255, 255, 255, 255))
        draw.rectangle((19, 27, 45, 35), fill=(255, 255, 255, 255))
    elif kind == 'rapid_fire':
        draw.polygon(
            ((35, 14), (19, 34), (30, 34), (24, 49), (46, 26), (35, 26)),
            fill=(255, 255, 255, 255),
        )
    else:
        draw.arc((16, 14, 48, 48), 180, 360, fill=(255, 255, 255, 255), width=5)
        draw.line((16, 30, 20, 43, 32, 51, 44, 43, 48, 30),
                  fill=(255, 255, 255, 255), width=5)
    return image


class PowerUp(arcade.Sprite):
    def __init__(self, kind: str, x: float, y: float):
        super().__init__(arcade.Texture(_power_up_image(kind)), 1.0)
        self.kind = kind
        self.center_x = x
        self.center_y = y
        self.base_y = y
        self._time = 0.0

    def update(self, delta_time: float = 1 / 60):
        self._time += delta_time
        self.center_y = self.base_y + math.sin(self._time * 3.5) * 5
        self.angle = math.sin(self._time * 2.5) * 4
