import arcade
import random
from player import Player
from coin import Coin, SpecialCoin
from enemy import Enemy, PinkMan
from name_view import NameView
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    PLAYER_MAX_HEALTH, PLAYER_SCALE, PLAYER_SPEED,
    TILE_SIZE, GRAVITY, COIN_SCALE
)

TOTAL_STATIC_COINS = 25


def tile_to_px(tile_x, tile_y, map_height_tiles=25):
    px = tile_x * TILE_SIZE * 2
    py = (map_height_tiles - tile_y) * TILE_SIZE * 2
    return px, py


class GameView(arcade.View):
    def __init__(self, player_name: str, window=None):
        super().__init__(window)
        self.keys_pressed = set()
        self.tempo = 0.0
        self.collected_coins = 0
        self.alert_timer = 0.0

        # câmera + tremor de tela
        self.camera = arcade.Camera2D()
        self.camera_center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.camera.position = self.camera_center
        self.shake_time = 0.0
        self.shake_duration = 0.0
        self.shake_amplitude = 0.0

        self.player = Player(
            '../sprites/Frog/frog.png', PLAYER_SCALE, PLAYER_SPEED, PLAYER_MAX_HEALTH, player_name
        )
        self.player.center_x = 200
        self.player.center_y = 300
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        # moedas
        self.coins = arcade.SpriteList()
        self.special_coins = arcade.SpriteList()

        # inimigos
        self.enemies = arcade.SpriteList()
        self.enemy_physics = []

        # tilemap
        self.tile_map = arcade.load_tilemap('../sprites/map/level_1.tmx', scaling=2.0)
        self.static_objects = self.tile_map.sprite_lists['Plataforms']
        self.background     = self.tile_map.sprite_lists['Background']

        # física do player
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            walls=self.static_objects,
            gravity_constant=GRAVITY
        )

        self._spawn_static_coins()
        self._spawn_special_coin()
        self._spawn_enemies()

        # HUD
        self.score_label = arcade.Text(
            text='Score: 0',
            x=10, y=SCREEN_HEIGHT - 30,
            color=arcade.color.RED_DEVIL,
            font_size=16, bold=True
        )
        self.timer_label = arcade.Text(
            text='Tempo: 0s',
            x=10, y=SCREEN_HEIGHT - 60,
            color=arcade.color.WHITE,
            font_size=16,
        )
        self.alert_label = arcade.Text(
            text='',
            x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2,
            color=arcade.color.RED,
            font_size=28, bold=True,
            anchor_x='center',
        )

    def _spawn_static_coins(self):
        tentativas_max = 200
        geradas = 0
        tentativas = 0

        while geradas < TOTAL_STATIC_COINS and tentativas < tentativas_max:
            tentativas += 1
            coin = Coin('../sprites/Coin_tiles.png', COIN_SCALE, 1)
            coin.center_x = random.randint(50, SCREEN_WIDTH - 50)
            coin.center_y = random.randint(200, SCREEN_HEIGHT - 50)

            if not arcade.check_for_collision_with_list(coin, self.static_objects):
                self.coins.append(coin)
                geradas += 1

    def _spawn_special_coin(self):
        sc = SpecialCoin(scale=COIN_SCALE)
        sc.center_x = random.randint(100, SCREEN_WIDTH - 100)
        sc.center_y = random.randint(300, SCREEN_HEIGHT - 100)
        self.special_coins.append(sc)

    def _spawn_enemies(self):
        ninja = Enemy(scale=2.0, speed=2.0)
        ninja.center_x = 800
        ninja.center_y = 400
        self.enemies.append(ninja)
        self.enemy_physics.append(
            arcade.PhysicsEnginePlatformer(ninja, walls=self.static_objects, gravity_constant=GRAVITY)
        )

        pinkman = PinkMan(scale=2.0, speed=1.2)
        pinkman.center_x = 400
        pinkman.center_y = 400
        self.enemies.append(pinkman)
        self.enemy_physics.append(
            arcade.PhysicsEnginePlatformer(pinkman, walls=self.static_objects, gravity_constant=GRAVITY)
        )

    def start_shake(self, amplitude: float = 10.0, duration: float = 0.3):
        self.shake_amplitude = amplitude
        self.shake_duration = duration
        self.shake_time = duration

    def _update_shake(self, delta_time: float):
        cx, cy = self.camera_center
        if self.shake_time > 0:
            self.shake_time -= delta_time
            fator = max(self.shake_time, 0) / self.shake_duration
            a = self.shake_amplitude * fator
            self.camera.position = (
                cx + random.uniform(-a, a),
                cy + random.uniform(-a, a),
            )
        else:
            self.camera.position = (cx, cy)

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        self.player.on_key_press(key)
        if key == arcade.key.ESCAPE:
            from menu_view import MenuView
            self.window.show_view(MenuView())

    def on_key_release(self, key, modifiers):
        self.keys_pressed.discard(key)
        self.player.on_key_release(key)

    def on_draw(self):
        self.clear()

        # mundo (treme junto com a câmera)
        with self.camera.activate():
            self.background.draw()
            self.static_objects.draw()
            self.enemies.draw()
            self.player_list.draw()
            self.coins.draw()
            self.special_coins.draw()

        # HUD (fixo, não treme)
        self.score_label.draw()
        self.timer_label.draw()

        if self.alert_timer > 0:
            self.alert_label.draw()

        arcade.draw_lrbt_rectangle_filled(
            SCREEN_WIDTH - 210, SCREEN_WIDTH - 10,
            SCREEN_HEIGHT - 40, SCREEN_HEIGHT - 20,
            arcade.color.GRAY
        )
        hp_width = 200 * (self.player.health / self.player.max_health)
        arcade.draw_lrbt_rectangle_filled(
            SCREEN_WIDTH - 210, SCREEN_WIDTH - 210 + hp_width,
            SCREEN_HEIGHT - 40, SCREEN_HEIGHT - 20,
            arcade.color.RED
        )

    def on_update(self, delta_time):
        self.tempo += delta_time
        self._update_shake(delta_time)

        if self.alert_timer > 0:
            self.alert_timer -= delta_time

        self.player_list.update(delta_time, self.keys_pressed)
        self.physics_engine.update()
        on_ground = self.physics_engine.can_jump()
        self.player.is_on_ground = on_ground
        if on_ground:
            self.player.jumps_remaining = 2

        for i, enemy in enumerate(self.enemies):
            enemy.update(delta_time, player=self.player, walls=self.static_objects)
            self.enemy_physics[i].update()
            enemy.is_on_ground = self.enemy_physics[i].can_jump()
            if enemy.is_on_ground:
                enemy.jumps_remaining = 1

        self.coins.update(delta_time)
        self.special_coins.update(delta_time)

        for coin in arcade.check_for_collision_with_list(self.player, self.coins):
            self.player.score += coin.value
            self.collected_coins += 1
            coin.remove_from_sprite_lists()

        for sc in arcade.check_for_collision_with_list(self.player, self.special_coins):
            self.player.score += sc.value
            sc.remove_from_sprite_lists()
            self._spawn_special_coin()

        for enemy in arcade.check_for_collision_with_list(self.player, self.enemies):
            enemy_x = enemy.center_x  # antes do on_hit_player (PinkMan teleporta)
            if enemy.on_hit_player(self.player):
                self.player.apply_knockback(enemy_x)
                self.start_shake()
                self.alert_label.text = '- 1 PONTO!'
                self.alert_timer = 1.0

        self.score_label.text = f'Score: {self.player.score}'
        self.timer_label.text = f'Tempo: {self.tempo:.1f}s'

        if self.collected_coins >= TOTAL_STATIC_COINS and len(self.coins) == 0:
            from game_over_view import GameOverView
            self.window.show_view(GameOverView(
                score=self.player.score,
                max_score=TOTAL_STATIC_COINS,
                tempo=self.tempo,
                nome=self.player.name,
            ))