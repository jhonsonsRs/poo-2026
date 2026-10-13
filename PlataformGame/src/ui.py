"""Visual compartilhado das telas de menu (estilo platformer / pixel art).

Tudo que é "bonito" mora aqui: fonte, cenário, painéis, botões, teclas,
títulos e rodapé. As views só montam o layout.
"""
import math
import os
import random

import arcade
from PIL import Image, ImageDraw, ImageFont

from constants import SCREEN_WIDTH, SCREEN_HEIGHT

W, H = SCREEN_WIDTH, SCREEN_HEIGHT
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(BASE_DIR, 'fonts')

# ---------------------------------------------------------------- paleta
INK = (43, 38, 64, 255)          # contorno / texto escuro
INK_SOFT = (122, 104, 104, 255)  # texto secundário (sobre papel)
CREAM = (255, 243, 214, 255)     # "papel" dos painéis
CREAM_DK = (240, 220, 172, 255)
WHITE = (255, 255, 255, 255)
MUTED = INK_SOFT
GOLD = (255, 200, 60, 255)
ORANGE = (214, 98, 48, 255)
SILVER = (214, 224, 238, 255)
BRONZE = (232, 168, 118, 255)
RED = (214, 64, 64, 255)
DARK = INK

KINDS = {
    'primary': (66, 134, 228),
    'success': (84, 182, 88),
    'danger': (222, 82, 82),
}

# ----------------------------------------------------------------- fonte
FONT = ('Poppins', 'Segoe UI', 'Arial')


def load_fonts():
    for nome in ('Poppins-Regular.ttf', 'Poppins-Bold.ttf'):
        try:
            arcade.load_font(os.path.join(FONT_DIR, nome))
        except Exception:
            pass  # sem a fonte, cai no Segoe UI / Arial


load_fonts()


def T(text, x, y, size, color=INK, bold=False, ax='center', ay='center'):
    """Atalho para arcade.Text com a fonte do jogo."""
    return arcade.Text(
        text, x, y, color, size,
        font_name=FONT, bold=bold, anchor_x=ax, anchor_y=ay,
    )


def text_width(t):
    try:
        return t.content_width
    except Exception:
        return len(t.text) * t.font_size * 0.6


# ------------------------------------------------------- imagens (Pillow)
SS = 3  # supersampling para bordas lisas


def _even(n):
    n = int(round(n))
    return n + (n % 2)


def _lighten(c, v):
    return tuple(min(255, x + v) for x in c[:3])


def block_image(w, h, fill, r=10, outline=INK, ow=4, shadow=(0, 6),
                shine=False):
    """Bloco "chunky": cor chapada + contorno grosso + sombra dura.

    shadow=(dx, dy) em pixels (dy positivo = para baixo). A imagem tem
    margem para a sombra e fica centrada no mesmo ponto do bloco.
    """
    w, h = _even(w), _even(h)
    dx, dy = shadow
    pad = _even(max(abs(dx), abs(dy), 2) + 2)
    cw, ch = w + 2 * pad, h + 2 * pad
    big = (cw * SS, ch * SS)
    img = Image.new('RGBA', big, tuple(outline[:3]) + (0,))
    d = ImageDraw.Draw(img)

    def rect(ox, oy, **kw):
        d.rounded_rectangle(
            ((pad + ox) * SS, (pad + oy) * SS,
             (pad + ox + w) * SS - 1, (pad + oy + h) * SS - 1),
            r * SS, **kw)

    if dx or dy:
        rect(dx, dy, fill=outline)
    rect(0, 0, fill=fill, outline=outline, width=ow * SS)
    if shine:
        # faixa clara no topo (dá volume sem degradê)
        sh = tuple(min(255, c + 46) for c in fill[:3])
        d.rounded_rectangle(
            ((pad + ow + 3) * SS, (pad + ow + 3) * SS,
             (pad + w - ow - 3) * SS, (pad + ow + 9) * SS),
            3 * SS, fill=sh)
    return img.resize((cw, ch), Image.LANCZOS)


def rounded_image(w, h, r, fill, outline=None, ow=2):
    """Retângulo arredondado chapado (sem sombra)."""
    w, h = _even(w), _even(h)
    big = (w * SS, h * SS)
    img = Image.new('RGBA', big, tuple(fill[:3]) + (0,))
    ImageDraw.Draw(img).rounded_rectangle(
        (0, 0, big[0] - 1, big[1] - 1), r * SS, fill=fill,
        outline=outline, width=ow * SS if outline else 0)
    return img.resize((w, h), Image.LANCZOS)


def circle_image(d, fill, outline=INK, ow=3):
    d = _even(d)
    size = d * SS
    img = Image.new('RGBA', (size, size), tuple(fill[:3]) + (0,))
    ImageDraw.Draw(img).ellipse((0, 0, size - 1, size - 1), fill=fill,
                                outline=outline, width=ow * SS)
    return img.resize((d, d), Image.LANCZOS)


_font_cache = {}


def _pil_font(px, bold=True):
    key = (px, bold)
    if key not in _font_cache:
        nome = 'Poppins-Bold.ttf' if bold else 'Poppins-Regular.ttf'
        try:
            _font_cache[key] = ImageFont.truetype(
                os.path.join(FONT_DIR, nome), px)
        except Exception:
            _font_cache[key] = ImageFont.load_default()
    return _font_cache[key]


def title_image(text, size, fill, ow=None, drop=None):
    """Texto grande com contorno grosso e sombra dura (estilo cartoon)."""
    px = int(size * 4 / 3)
    ow = ow or max(4, px // 9)
    drop = drop or max(4, px // 8)
    font = _pil_font(px)
    l, t, r, b = font.getbbox(text, stroke_width=ow)
    tw, th = r - l, b - t
    pad = 6
    cw, ch = _even(tw + 2 * pad), _even(th + drop + 2 * pad)
    ox, oy = pad - l, pad - t
    img = Image.new('RGBA', (cw, ch), tuple(INK[:3]) + (0,))
    d = ImageDraw.Draw(img)
    d.text((ox, oy + drop), text, font=font, fill=INK,
           stroke_width=ow, stroke_fill=INK)
    d.text((ox, oy), text, font=font, fill=fill,
           stroke_width=ow, stroke_fill=INK)
    return img


_keycap_cache = {}


def keycap_image(w, h, symbol=None):
    """Tecla de teclado. symbol: None, 'left' ou 'right' (setas)."""
    key = (w, h, symbol)
    if key in _keycap_cache:
        return _keycap_cache[key]
    w, h = _even(w), _even(h)
    depth = 4
    size = (w * SS, (h + depth) * SS)
    img = Image.new('RGBA', size, tuple(INK[:3]) + (0,))
    d = ImageDraw.Draw(img)
    r = 7 * SS
    d.rounded_rectangle((0, depth * SS, size[0] - 1, size[1] - 1), r,
                        fill=INK)
    d.rounded_rectangle((0, 0, size[0] - 1, h * SS - 1), r,
                        fill=CREAM, outline=INK, width=3 * SS)
    if symbol:
        cx, cy = size[0] / 2, h * SS / 2
        s = 7 * SS
        if symbol == 'left':
            pts = [(cx + s * 0.8, cy - s), (cx + s * 0.8, cy + s),
                   (cx - s * 1.0, cy)]
        else:
            pts = [(cx - s * 0.8, cy - s), (cx - s * 0.8, cy + s),
                   (cx + s * 1.0, cy)]
        d.polygon(pts, fill=INK)
    img = img.resize((w, h + depth), Image.LANCZOS)
    _keycap_cache[key] = img
    return img


# --------------------------------------------------------------- sprites
def make_sprite(img, cx, cy):
    s = arcade.Sprite(arcade.Texture(img))
    s.center_x = cx
    s.center_y = cy
    return s


class Layer:
    """Sprites (embaixo) + textos (em cima), desenhados juntos."""

    def __init__(self):
        self.sprites = arcade.SpriteList()
        self.texts = []

    def image(self, img, cx, cy):
        s = make_sprite(img, cx, cy)
        self.sprites.append(s)
        return s

    def text(self, *args, **kwargs):
        t = T(*args, **kwargs)
        self.texts.append(t)
        return t

    def panel(self, cx, cy, w, h):
        """Painel de "papel" com contorno grosso e sombra dura."""
        self.image(block_image(w, h, CREAM, r=14, ow=4, shadow=(0, 8)),
                   cx, cy - 4)

    def keycap(self, label, cx, cy, w=None, h=40, size=16, symbol=None):
        """Adiciona uma tecla centrada em (cx, cy). Retorna a largura."""
        if w is None:
            w = 44 if len(label) <= 1 else 16 + 11 * len(label)
        w = _even(w)
        self.image(keycap_image(w, h, symbol), cx, cy - 2)
        if label and not symbol:
            self.text(label, cx, cy, size, INK, bold=True)
        return w

    def draw(self):
        self.sprites.draw()
        for t in self.texts:
            t.draw()


# --------------------------------------------------------------- cenário
PX = 4  # cada "pixel" do cenário vale 4x4 pixels da tela
GW, GH = W // PX, H // PX
GROUND = 22  # altura do chão, em "pixels" do cenário


def _scenery_image():
    img = Image.new('RGBA', (GW, GH), (0, 0, 0, 255))
    d = ImageDraw.Draw(img)

    # céu em faixas
    sky = [(86, 178, 238), (104, 190, 242), (124, 202, 246),
           (146, 214, 248), (168, 224, 250), (190, 234, 252)]
    band = GH / len(sky)
    for i, c in enumerate(sky):
        d.rectangle((0, int(i * band), GW, int((i + 1) * band)), fill=c)

    top = GH - GROUND
    # morros ao fundo (duas camadas)
    for base, amp, col, ph in ((26, 9, (120, 200, 186), 0.0),
                               (16, 7, (96, 178, 150), 2.1)):
        for x in range(GW):
            h = base + amp * math.sin(x / 21 + ph) \
                + amp * 0.5 * math.sin(x / 8 + ph * 2)
            d.line((x, top - int(h), x, top), fill=col)

    # moitas
    rnd = random.Random(3)
    for cx in (24, 82, 190, 252, 300):
        r = rnd.randint(6, 9)
        for dx, rr in ((-r, r * .8), (0, r), (r, r * .8)):
            d.ellipse((cx + dx - rr, top - rr * 1.5, cx + dx + rr, top + 2),
                      fill=(76, 164, 80), outline=(44, 112, 60))

    # chão: grama + terra com detalhes
    d.rectangle((0, top, GW, GH), fill=(150, 104, 70))
    d.rectangle((0, top, GW, top + 3), fill=(110, 196, 80))
    d.rectangle((0, top + 3, GW, top + 4), fill=(70, 140, 56))
    d.line((0, top, GW, top), fill=(150, 226, 104))
    for _ in range(170):
        x, y = rnd.randint(0, GW - 2), rnd.randint(top + 6, GH - 1)
        d.rectangle((x, y, x + 1, y), fill=(122, 82, 56))
    for _ in range(60):
        x, y = rnd.randint(0, GW - 1), rnd.randint(top + 6, GH - 1)
        d.point((x, y), fill=(176, 126, 88))
    return img.resize((W, H), Image.NEAREST)


def _cloud_image(units, seed):
    rnd = random.Random(seed)
    w, h = units, units // 2 + 4
    img = Image.new('RGBA', (w, h), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)
    n = 3 + units // 14
    for i in range(n):
        r = rnd.randint(units // 8, units // 5)
        cx = int((i + .5) * (w - 2 * r) / n + r)
        cy = h - 5 - r // 2
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, 255))
    d.rectangle((2, h - 9, w - 3, h - 5), fill=(255, 255, 255, 255))
    # sombra azulada embaixo
    d.rectangle((2, h - 5, w - 3, h - 4), fill=(206, 230, 248, 255))
    return img.resize((w * PX, h * PX), Image.NEAREST)


class Background:
    """Cenário de platformer: céu, morros, grama e nuvens passando."""

    def __init__(self):
        self.sprites = arcade.SpriteList()
        self.sprites.append(make_sprite(_scenery_image(), W / 2, H / 2))
        self.clouds = arcade.SpriteList()
        self.cloud_info = []  # (velocidade, largura)
        # (largura em px do cenário, seed, x, y, velocidade)
        for units, seed, x, y, v in ((34, 1, 200, 600, 9),
                                     (24, 2, 900, 676, 6),
                                     (42, 3, 1100, 540, 12),
                                     (20, 4, 480, 500, 5)):
            img = _cloud_image(units, seed)
            self.clouds.append(make_sprite(img, x, y))
            self.cloud_info.append((v, img.size[0]))

    def update(self, dt):
        for s, (v, w) in zip(self.clouds, self.cloud_info):
            s.center_x += v * dt
            if s.center_x - w / 2 > W:
                s.center_x = -w / 2

    def draw(self):
        self.sprites.draw()
        self.clouds.draw()


_background = None


def get_background():
    """Um único cenário para todas as telas (as nuvens não "reiniciam")."""
    global _background
    if _background is None:
        _background = Background()
    return _background


# ---------------------------------------------------------------- título
class Title:
    """Título grande com contorno grosso e sombra (estilo cartoon)."""

    def __init__(self, text, cx, cy, size=40, color=WHITE, bar=False):
        self.sprites = arcade.SpriteList()
        self.sprites.append(make_sprite(title_image(text, size, color),
                                        cx, cy - 3))

    def draw(self):
        self.sprites.draw()


# ---------------------------------------------------------------- botão
_button_cache = {}
LIFT = 3  # quanto o botão "sobe" quando está em foco


def _button_image(w, h, kind, active, hint_w):
    key = (w, h, kind, active, hint_w)
    if key in _button_cache:
        return _button_cache[key]
    cor = KINDS[kind]
    if active:
        cor = _lighten(cor, 34)
    img = block_image(w, h, cor + (255,), r=12, ow=4, shadow=(0, 6),
                      shine=True)
    if hint_w:
        pad = (img.size[0] - _even(w)) // 2
        ch = 30
        chip = block_image(hint_w, ch, INK, r=7, ow=2, shadow=(0, 0))
        cpad = (chip.size[0] - _even(hint_w)) // 2
        img.alpha_composite(
            chip, (pad + 14 - cpad, pad + (_even(h) - ch) // 2 - cpad))
    _button_cache[key] = img
    return img


class Button:
    def __init__(self, label, cx, cy, w=360, h=54, hint=None,
                 kind='primary', size=20):
        self.cx, self.cy, self.w, self.h = cx, cy, w, h
        self.active = False
        hint_w = None
        if hint:
            hint_w = 30 if len(hint) <= 1 else 14 + 9 * len(hint)
        self._normal = arcade.SpriteList()
        self._active = arcade.SpriteList()
        self._normal.append(make_sprite(
            _button_image(w, h, kind, False, hint_w), cx, cy - 3))
        self._active.append(make_sprite(
            _button_image(w, h, kind, True, hint_w), cx, cy - 3 + LIFT))

        self._shift = (hint_w + 6) / 2 if hint_w else 0
        lx = cx + self._shift
        self.label_shadow = T(label, lx, cy - 2, size, INK, bold=True)
        self.label = T(label, lx, cy, size, WHITE, bold=True)
        self.hint = None
        if hint:
            hx = cx - w / 2 + 14 + hint_w / 2
            self.hint = T(hint, hx, cy, 13, GOLD, bold=True)

    def contains(self, x, y):
        return (abs(x - self.cx) <= self.w / 2
                and abs(y - self.cy) <= self.h / 2)

    def draw(self):
        up = LIFT if self.active else 0
        (self._active if self.active else self._normal).draw()
        self.label_shadow.y = self.cy - 2 + up
        self.label.y = self.cy + up
        self.label_shadow.draw()
        self.label.draw()
        if self.hint:
            self.hint.y = self.cy + up
            self.hint.draw()


# ---------------------------------------------------------------- rodapé
class Footer:
    """Linha de atalhos sobre o chão: [M] Menu Principal   [ESC] Sair"""

    def __init__(self, items, y=50, gap=34):
        self.layer = Layer()
        parts = []
        for key, desc in items:
            kw = _even(max(36, 16 + 11 * len(key)))
            d = T(desc, 0, y, 15, CREAM, ax='left')
            parts.append((key, kw, d, text_width(d)))
        total = sum(kw + 12 + dw for _, kw, _, dw in parts)
        total += gap * (len(parts) - 1)
        x = W / 2 - total / 2
        for key, kw, d, dw in parts:
            self.layer.image(keycap_image(kw, 30), round(x + kw / 2), y - 2)
            self.layer.text(key, x + kw / 2, y, 13, INK, bold=True)
            d.x = x + kw + 12
            self.layer.texts.append(d)
            x += kw + 12 + dw + gap

    def draw(self):
        self.layer.draw()
