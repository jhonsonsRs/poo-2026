"""Gera os áudios do jogo (músicas e efeitos) em sounds/*.wav, sem depender de arquivos externos.

Rode uma vez:  python gerar_audios.py
"""
import math
import os
import random
import struct
import wave

SR = 22050
PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sounds')

NOTAS = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6,
         'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}


def freq(nome):
    """'A4' -> 440.0"""
    n, o = nome[:-1], int(nome[-1])
    semitons = NOTAS[n] + 12 * (o - 4) - 9
    return 440.0 * 2 ** (semitons / 12)


def onda(tipo, fase):
    f = fase % 1.0
    if tipo == 'sine':
        return math.sin(2 * math.pi * f)
    if tipo == 'square':
        return 1.0 if f < 0.5 else -1.0
    if tipo == 'pulse':
        return 1.0 if f < 0.25 else -1.0
    if tipo == 'tri':
        return 4 * abs(f - 0.5) - 1
    if tipo == 'saw':
        return 2 * f - 1
    raise ValueError(tipo)


def tom(buf, inicio, dur, f0, tipo='square', vol=0.3, f1=None, ataque=0.005,
        release=0.6):
    """Soma uma nota no buffer. f1 faz glissando; release = fração final que decai."""
    i0 = int(inicio * SR)
    n = int(dur * SR)
    fase = 0.0
    for k in range(n):
        if i0 + k >= len(buf):
            break
        t = k / SR
        f = f0 if f1 is None else f0 + (f1 - f0) * (k / n)
        fase += f / SR
        env = min(1.0, t / ataque) if ataque else 1.0
        rel = max(1e-9, dur * release)
        if t > dur - rel:
            env *= max(0.0, (dur - t) / rel)
        buf[i0 + k] += onda(tipo, fase) * vol * env


def ruido(buf, inicio, dur, vol=0.2, decai=8.0):
    i0 = int(inicio * SR)
    n = int(dur * SR)
    for k in range(n):
        if i0 + k >= len(buf):
            break
        buf[i0 + k] += (random.random() * 2 - 1) * vol * math.exp(-decai * k / n)


def bumbo(buf, inicio, vol=0.5):
    tom(buf, inicio, 0.18, 150, 'sine', vol, f1=45, ataque=0.0, release=0.9)


def salvar(nome, buf, pico=0.85):
    m = max(1e-9, max(abs(x) for x in buf))
    g = pico / m if m > pico else 1.0
    os.makedirs(PASTA, exist_ok=True)
    with wave.open(os.path.join(PASTA, nome + '.wav'), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(b''.join(struct.pack('<h', int(x * g * 32767)) for x in buf))
    print('ok', nome)


def novo(seg):
    return [0.0] * int(seg * SR)


# ------------------------------------------------------------- músicas
def musica_menu():
    """Calma e flutuante: 80 bpm, Dó maior, 8 compassos (loop sem emendas)."""
    bpm = 80
    beat = 60 / bpm
    compassos = 8
    buf = novo(compassos * 4 * beat)
    acordes = [('C3', ['C4', 'E4', 'G4', 'E4']),
               ('A2', ['A3', 'C4', 'E4', 'C4']),
               ('F2', ['F3', 'A3', 'C4', 'A3']),
               ('G2', ['G3', 'B3', 'D4', 'B3'])] * 2
    for c, (baixo, arp) in enumerate(acordes):
        t0 = c * 4 * beat
        tom(buf, t0, 4 * beat, freq(baixo), 'tri', 0.30, release=0.3)
        for i in range(8):                       # arpejo em colcheias
            nota = arp[i % 4]
            tom(buf, t0 + i * beat / 2, beat * 0.9, freq(nota), 'tri', 0.16,
                release=0.8)
    melodia = ['E5', 'G5', 'A5', 'G5', 'E5', 'D5', 'C5', None,
               'D5', 'E5', 'G5', 'E5', 'D5', 'C5', 'D5', None]
    for i, nota in enumerate(melodia):           # melodia nos compassos 5-8
        if nota:
            tom(buf, 16 * beat + i * 2 * beat, beat * 1.8, freq(nota), 'sine',
                0.20, ataque=0.03, release=0.7)
    salvar('musica_menu', buf)


def musica_jogo():
    """Rápida e animada: 150 bpm, Lá menor, 8 compassos, bateria e baixo pulsante."""
    bpm = 150
    beat = 60 / bpm
    compassos = 8
    buf = novo(compassos * 4 * beat)
    prog = [('A2', ['A4', 'C5', 'E5']), ('F2', ['F4', 'A4', 'C5']),
            ('C3', ['C5', 'E5', 'G5']), ('G2', ['G4', 'B4', 'D5'])] * 2
    for c, (baixo, arp) in enumerate(prog):
        t0 = c * 4 * beat
        for i in range(8):                       # baixo em colcheias
            tom(buf, t0 + i * beat / 2, beat * 0.45, freq(baixo), 'pulse', 0.22,
                release=0.5)
        for i in range(16):                      # arpejo em semicolcheias
            tom(buf, t0 + i * beat / 4, beat * 0.22, freq(arp[i % 3]), 'square',
                0.07, release=0.6)
        for b in range(4):                       # bateria
            tb = t0 + b * beat
            if b in (0, 2):
                bumbo(buf, tb)
            else:
                ruido(buf, tb, 0.12, 0.30, decai=7)
            ruido(buf, tb, 0.04, 0.10, decai=10)
            ruido(buf, tb + beat / 2, 0.04, 0.08, decai=10)
    melodia = [('A5', 1), ('C6', 1), ('B5', 1), ('A5', 1), ('G5', 2), ('E5', 2),
               ('F5', 1), ('A5', 1), ('G5', 1), ('F5', 1), ('E5', 2), ('C5', 2),
               ('C6', 1), ('B5', 1), ('C6', 1), ('D6', 1), ('E6', 2), ('G5', 2),
               ('D6', 1), ('B5', 1), ('G5', 1), ('B5', 1), ('D6', 2), ('B5', 2)]
    t = 16 * beat                                # melodia nos compassos 5-8
    for nota, dur in melodia:
        if t >= len(buf) / SR - 1e-6:
            break
        tom(buf, t, dur * beat * 0.9, freq(nota), 'square', 0.13, release=0.4)
        t += dur * beat
    salvar('musica_jogo', buf)


# ------------------------------------------------------------- efeitos
def fx_pulo():
    b = novo(0.18)
    tom(b, 0, 0.18, 280, 'square', 0.35, f1=720, release=0.4)
    salvar('pulo', b)


def fx_mosca():
    b = novo(0.16)
    tom(b, 0, 0.07, freq('B5'), 'square', 0.30, release=0.3)
    tom(b, 0.06, 0.10, freq('E6'), 'square', 0.30, release=0.6)
    salvar('mosca', b)


def fx_mosca_especial():
    b = novo(0.4)
    for i, n in enumerate(['C5', 'E5', 'G5', 'C6', 'E6']):
        tom(b, i * 0.07, 0.12, freq(n), 'square', 0.28, release=0.6)
    salvar('mosca_especial', b)


def fx_dano():
    b = novo(0.35)
    tom(b, 0, 0.35, 330, 'saw', 0.35, f1=70, release=0.5)
    ruido(b, 0, 0.18, 0.35, decai=6)
    salvar('dano', b)


def fx_vitoria():
    b = novo(1.6)
    seq = [('C5', 0.00, 0.14), ('E5', 0.14, 0.14), ('G5', 0.28, 0.14),
           ('C6', 0.42, 0.30), ('G5', 0.76, 0.12), ('C6', 0.88, 0.12),
           ('E6', 1.00, 0.55)]
    for n, t0, d in seq:
        tom(b, t0, d, freq(n), 'square', 0.25, release=0.5)
        tom(b, t0, d, freq(n) / 2, 'tri', 0.25, release=0.5)
    salvar('vitoria', b)


def fx_navegar():
    b = novo(0.06)
    tom(b, 0, 0.06, 660, 'square', 0.22, release=0.6)
    salvar('navegar', b)


def fx_selecionar():
    b = novo(0.2)
    tom(b, 0, 0.07, freq('E5'), 'square', 0.28, release=0.3)
    tom(b, 0.07, 0.13, freq('A5'), 'square', 0.28, release=0.7)
    salvar('selecionar', b)


def fx_tecla():
    b = novo(0.04)
    tom(b, 0, 0.04, 900, 'tri', 0.25, release=0.8)
    salvar('tecla', b)


def fx_erro():
    b = novo(0.25)
    tom(b, 0, 0.12, 180, 'saw', 0.30, release=0.3)
    tom(b, 0.12, 0.13, 140, 'saw', 0.30, release=0.6)
    salvar('erro', b)


if __name__ == '__main__':
    random.seed(7)
    musica_menu()
    musica_jogo()
    for f in (fx_pulo, fx_mosca, fx_mosca_especial, fx_dano, fx_vitoria,
              fx_navegar, fx_selecionar, fx_tecla, fx_erro):
        f()
