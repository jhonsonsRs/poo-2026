from pathlib import Path

from pyglet.image import load
from pyglet.window import ImageMouseCursor


_cursor = None


def set_default_cursor(window):
    global _cursor
    if _cursor is None:
        path = Path(__file__).resolve().parent.parent / 'sprites' / 'light_cursor.png'
        image = load(str(path))
        _cursor = ImageMouseCursor(image, hot_x=0, hot_y=31)
    window.set_mouse_cursor(_cursor)
