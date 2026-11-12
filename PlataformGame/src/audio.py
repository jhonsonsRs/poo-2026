"""Gerenciador de áudio: músicas em loop (menu e jogo) e efeitos sonoros.

Se o áudio falhar (sem placa de som, arquivo ausente), o jogo continua mudo.
"""
import os

import arcade

PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sounds')

VOLUME_MUSICA = 0.35
VOLUME_SFX = {
    'pulo': 0.5, 'mosca': 0.6, 'mosca_especial': 0.7, 'dano': 0.7,
    'vitoria': 0.8, 'navegar': 0.4, 'selecionar': 0.6, 'tecla': 0.3,
    'erro': 0.6,
}

_cache = {}
_player_musica = None
_musica_atual = None


def _carregar(nome):
    if nome not in _cache:
        try:
            _cache[nome] = arcade.load_sound(os.path.join(PASTA, nome + '.wav'))
        except Exception as erro:
            print(f'[audio] não foi possível carregar "{nome}": {erro}')
            _cache[nome] = None
    return _cache[nome]


def sfx(nome):
    som = _carregar(nome)
    if som is None:
        return
    try:
        arcade.play_sound(som, volume=VOLUME_SFX.get(nome, 0.6))
    except Exception as erro:
        print(f'[audio] erro ao tocar "{nome}": {erro}')


def tocar_musica(nome):
    """Toca a música em loop. Se já é a atual, não reinicia (menus compartilham a música)."""
    global _player_musica, _musica_atual
    if nome == _musica_atual and _player_musica is not None:
        return
    parar_musica()
    som = _carregar('musica_' + nome)
    if som is None:
        return
    try:
        _player_musica = arcade.play_sound(som, volume=VOLUME_MUSICA, loop=True)
        _musica_atual = nome
    except Exception as erro:
        print(f'[audio] erro ao tocar música "{nome}": {erro}')


def parar_musica():
    global _player_musica, _musica_atual
    if _player_musica is not None:
        try:
            arcade.stop_sound(_player_musica)
        except Exception:
            pass
    _player_musica = None
    _musica_atual = None
