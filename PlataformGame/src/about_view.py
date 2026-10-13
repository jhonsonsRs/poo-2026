import os
import arcade
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from ui import (draw_crt, Layer, Title, Footer, get_background, make_sprite,
                FONT_DIR, INK, MUTED)

NOME = 'João Emanuel Vieira Orlando'
FOTO = 'profile.jpeg'
SS = 2


def _achar_foto():
    aqui = os.path.dirname(os.path.abspath(__file__))
    for pasta in ('../sprites', 'sprites', os.path.join(aqui, '..', 'sprites'),
                  os.path.join(aqui, 'sprites')):
        caminho = os.path.join(pasta, FOTO)
        if os.path.exists(caminho):
            return caminho
    return None


def _foto_ou_iniciais(caminho, size):
    """Foto recortada; se não existir, um círculo com as iniciais."""
    if caminho:
        return ImageOps.fit(Image.open(caminho).convert('RGBA'),
                            (size, size), Image.LANCZOS)
    img = Image.new('RGBA', (size, size), (92, 70, 214, 255))
    try:
        fonte = ImageFont.truetype(
            os.path.join(FONT_DIR, 'Poppins-Bold.ttf'), size // 3)
    except Exception:
        fonte = ImageFont.load_default()
    ImageDraw.Draw(img).text((size / 2, size / 2), 'JO', font=fonte,
                             fill=(255, 255, 255, 255), anchor='mm')
    return img


def make_avatar(caminho, size=360, ring=7, pad=12):
    """Foto circular com anel dourado e brilho suave."""
    total = size + 2 * ring + 2 * pad
    canvas = Image.new('RGBA', (total, total), (255, 196, 61, 0))

    # brilho dourado
    glow = Image.new('RGBA', (total, total), (255, 196, 61, 0))
    ImageDraw.Draw(glow).ellipse(
        (pad - 6, pad - 6, total - pad + 6, total - pad + 6),
        fill=(255, 196, 61, 0))
    glow = glow.filter(ImageFilter.GaussianBlur(14))
    canvas = Image.alpha_composite(canvas, glow)

    # anel + foto (em alta resolução, depois reduz para suavizar)
    big = total * SS
    layer = Image.new('RGBA', (big, big), (255, 196, 61, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse((pad * SS, pad * SS, (total - pad) * SS - 1,
               (total - pad) * SS - 1), fill=INK)
    inner = (size) * SS
    foto = _foto_ou_iniciais(caminho, inner)
    mask = Image.new('L', (inner, inner), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, inner - 1, inner - 1), fill=255)
    foto.putalpha(mask)
    off = (pad + ring) * SS
    layer.alpha_composite(foto, (off, off))
    layer = layer.resize((total, total), Image.LANCZOS)
    return Image.alpha_composite(canvas, layer)


class AboutView(arcade.View):
    def __init__(self, window=None):
        super().__init__(window)
        self.bg = get_background()
        cx = SCREEN_WIDTH / 2
        self.titulo = Title('Sobre o Jogo', cx, SCREEN_HEIGHT - 60, size=38)
        self.rodape = Footer([('M', 'Voltar ao Menu'), ('ESC', 'Voltar')])

        L = self.layer = Layer()
        L.panel(cx, 390, 640, 380)
        L.text('DESENVOLVIDO POR', cx, 545, 13, MUTED, bold=True)

        avatar = make_avatar(_achar_foto())
        s = L.image(avatar, cx, 415)
        s.scale = 0.5

        L.text(NOME, cx + 0, 270, 24, INK, bold=True)

    def on_update(self, delta_time):
        self.bg.update(delta_time)

    def on_draw(self):
        self.clear()
        self.bg.draw()
        self.titulo.draw()
        self.layer.draw()
        self.rodape.draw()
        draw_crt()

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.ESCAPE, arcade.key.M):
            from menu_view import MenuView
            self.window.show_view(MenuView())
