import arcade
import random
import audio
from player import Player
from bloco import Bloco
from coin import Coin, SpecialCoin
from enemy import Enemy, PinkMan, VirtualGuy
from enemy_projectile import EnemyProjectile
from projectile import Projectile
from checkpoint import Checkpoint
from power_up import PowerUp
from boss import Boss
from particle import create_burst
from name_view import NameView
from ui import (
    crt_begin, draw_crt, update_crt, crt_glitch,
    Layer, Title, Button, WHITE, INK, MUTED,
)
from cursor import set_default_cursor
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    PLAYER_MAX_HEALTH, PLAYER_SCALE, PLAYER_SPEED,
    TILE_SIZE, GRAVITY, COIN_SCALE,
    TILEMAP_SCALE
)

TOTAL_STATIC_COINS = 12


def tile_to_px(tile_x, tile_y, map_height_tiles=25):
    px = tile_x * TILE_SIZE * 2
    py = (map_height_tiles - tile_y) * TILE_SIZE * 2
    return px, py


class GameView(arcade.View):
    def __init__(
        self, player_name: str, window=None, game_mode: str = 'quick'
    ):
        super().__init__(window)
        audio.tocar_musica('jogo')
        self.game_mode = game_mode
        self.keys_pressed = set()
        self.tempo = 0.0
        self.collected_coins = 0
        self.alert_timer = 0.0
        self.enemy_wave = 0
        self.enemy_respawn_timer = 0.0
        self.paused = False
        self.checkpoint_notice_timer = 0.0
        self.pause_panel = Layer()
        self.pause_panel.panel(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 760, 500)
        self.pause_title = Title(
            'JOGO PAUSADO', SCREEN_WIDTH / 2, 540, size=42, color=WHITE
        )
        self.pause_panel.text(
            'A aventura está pausada', SCREEN_WIDTH / 2, 478, 18, MUTED
        )
        self.pause_panel.text(
            'ESC ou P para continuar', SCREEN_WIDTH / 2, 445, 15, MUTED
        )
        self.pause_buttons = [
            Button(
                'Continuar', SCREEN_WIDTH / 2, 365,
                w=430, h=56, hint='ESC', kind='success', size=19
            ),
            Button(
                'Reiniciar', SCREEN_WIDTH / 2, 285,
                w=430, h=56, hint='R', kind='primary', size=19
            ),
            Button(
                'Menu Principal', SCREEN_WIDTH / 2, 205,
                w=430, h=56, hint='M', kind='danger', size=19
            ),
        ]
        self.checkpoint_notice_panel = Layer()
        self.checkpoint_notice_panel.panel(
            SCREEN_WIDTH / 2, 115, 500, 70
        )
        self.checkpoint_notice_text = self.checkpoint_notice_panel.text(
            '', SCREEN_WIDTH / 2, 115, 20, INK, bold=True
        )
        self.mouse_x = SCREEN_WIDTH / 2
        self.mouse_y = SCREEN_HEIGHT / 2
        set_default_cursor(self.window)

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
        self.projectiles = arcade.SpriteList()
        self.enemy_projectiles = arcade.SpriteList()
        self.particles = arcade.SpriteList()
        self.boss = None
        self.boss_list = arcade.SpriteList()
        self.boss_physics = None
        self.boss_active = False
        self.boss_arena_walls = arcade.SpriteList()
        self.boss_arena_left = 0.0
        self.boss_arena_right = 0.0
        self.boss_rewarded = False
        self.checkpoints = arcade.SpriteList()
        self.power_ups = arcade.SpriteList()
        self.last_checkpoint = None

        # inimigos
        self.enemies = arcade.SpriteList()
        self.enemy_physics = []

        # tilemap
        self.tile_map = arcade.load_tilemap('../sprites/map/level_1.tmx', scaling=2.0)
        self.background = self.tile_map.sprite_lists['Background']
        self.world_width = self.tile_map.width * TILE_SIZE * TILEMAP_SCALE
        self.world_height = self.tile_map.height * TILE_SIZE * TILEMAP_SCALE
        self.area_regions = self._build_area_regions()
        self.area_particles = self._build_area_particles()
        self.player.set_world_bounds(self.world_width, self.world_height)
        self.camera_center = self._camera_position()
        self.camera.position = self.camera_center

        # chão e plataformas: todos os sólidos do cenário são objetos Bloco
        self.blocos = self._construir_blocos()
        if self.game_mode == 'hardcore':
            self._spawn_checkpoints()
            self._spawn_power_ups()
            self._spawn_boss()
        self.walls = self._all_walls()
        if self.boss is not None:
            self.boss_physics = arcade.PhysicsEnginePlatformer(
                self.boss,
                walls=self.walls,
                gravity_constant=GRAVITY,
            )

        # física do player
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            walls=self.walls,
            gravity_constant=GRAVITY
        )

        self._spawn_static_coins()
        self._spawn_special_coin()
        self._spawn_enemies()
        # HUD
        self.score_label = arcade.Text(
            text='Score: 0',
            x=35, y=SCREEN_HEIGHT - 30,
            color=arcade.color.RED_DEVIL,
            font_size=20, bold=True
        )
        self.timer_label = arcade.Text(
            text='Tempo: 0s',
            x=35, y=SCREEN_HEIGHT - 60,
            color=arcade.color.WHITE,
            font_size=18,
        )
        self.alert_label = arcade.Text(
            text='',
            x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2,
            color=arcade.color.RED,
            font_size=28, bold=True,
            anchor_x='center',
        )

    def _construir_blocos(self) -> arcade.SpriteList:
        """Monta a SpriteList de Blocos: chão/plataformas do mapa + plataformas extras."""
        blocos = arcade.SpriteList(use_spatial_hash=True)
        camada = self.tile_map.sprite_lists['Plataforms']
        for tile in camada:
            blocos.append(Bloco.de_tile(tile))

        return blocos

    def _build_area_regions(self):
        if self.game_mode != 'hardcore':
            return ()
        width = self.world_width
        return (
            (0, width * 0.22, 'FLORESTA', (38, 92, 63, 42)),
            (width * 0.22, width * 0.42, 'CAVERNA', (38, 48, 82, 72)),
            (width * 0.42, width * 0.62, 'RUINAS', (94, 55, 93, 52)),
            (width * 0.62, width * 0.84, 'LABORATORIO', (24, 104, 116, 48)),
            (width * 0.84, width, 'ARENA FINAL', (116, 38, 49, 42)),
        )

    def _build_area_particles(self):
        if self.game_mode != 'hardcore':
            return ()
        rng = random.Random(2026)
        return tuple(
            (
                rng.uniform(0, self.world_width),
                rng.uniform(160, self.world_height - 40),
                rng.uniform(1.5, 3.5),
            )
            for _ in range(90)
        )

    def _draw_area_identity(self):
        if not self.area_regions:
            return
        camera_x, camera_y = self.camera.position
        view_left = camera_x - SCREEN_WIDTH / 2
        view_right = camera_x + SCREEN_WIDTH / 2
        for left, right, _, color in self.area_regions:
            if right < view_left or left > view_right:
                continue
            arcade.draw_lrbt_rectangle_filled(
                max(left, view_left),
                min(right, view_right),
                0,
                self.world_height,
                color,
            )
        for x, y, radius in self.area_particles:
            if view_left - 20 <= x <= view_right + 20:
                arcade.draw_circle_filled(
                    x, y, radius, (220, 245, 220, 45)
                )

    def _all_walls(self):
        walls = arcade.SpriteList()
        for wall in self.blocos:
            walls.append(wall)
        return walls

    def _spawn_checkpoints(self):
        checkpoint_positions = (
            1200, 2400, 3600, 4800, 6000, 7200, 8400, 9600
        )
        for x in checkpoint_positions:
            if x >= self.world_width:
                continue
            surfaces = [
                bloco.top for bloco in self.blocos
                if abs(bloco.center_x - x) <= bloco.width / 2
                and bloco.top <= 160
            ]
            if not surfaces:
                continue
            ground_top = max(surfaces)
            checkpoint = Checkpoint(x, ground_top + 56)
            self.checkpoints.append(checkpoint)

    def _show_checkpoint_notice(self, message: str):
        self.checkpoint_notice_text.text = message
        self.checkpoint_notice_timer = 1.5

    def _spawn_power_ups(self):
        power_up_positions = (
            ('health', 1800),
            ('rapid_fire', 3000),
            ('shield', 4200),
            ('health', 5700),
            ('rapid_fire', 6900),
            ('shield', 8100),
            ('health', 9300),
        )
        for kind, x in power_up_positions:
            if x >= self.world_width:
                continue
            surfaces = [
                bloco.top for bloco in self.blocos
                if abs(bloco.center_x - x) <= bloco.width / 2
                and bloco.top <= 160
            ]
            if surfaces:
                self.power_ups.append(PowerUp(kind, x, max(surfaces) + 45))

    def _spawn_boss(self):
        boss_x = self.world_width - 420
        self.boss_arena_left = boss_x - 700
        self.boss_arena_right = self.world_width - 80
        for x in (self.boss_arena_left, self.boss_arena_right):
            wall = arcade.SpriteSolidColor(
                24, 360, (0, 0, 0, 0)
            )
            wall.center_x = x
            wall.center_y = 180
            self.boss_arena_walls.append(wall)
        surfaces = [
            bloco.top for bloco in self.blocos
            if abs(bloco.center_x - boss_x) <= bloco.width / 2
            and bloco.top <= 160
        ]
        ground_top = max(surfaces, default=128)
        self.boss = Boss(boss_x, ground_top + 100)
        self.boss_list.append(self.boss)

    def _update_boss_activation(self):
        if (
            self.game_mode == 'hardcore'
            and self.boss is not None
            and not self.boss_active
            and self.player.center_x >= self.boss.center_x - 700
        ):
            self.boss_active = True
            self.boss_arena_walls[0].center_x = self.player.center_x - 100
            for wall in self.boss_arena_walls:
                self.walls.append(wall)
            self.player.center_x = max(
                self.player.center_x, self.boss_arena_left + 40
            )
            self._burst(
                self.player.center_x, self.player.center_y,
                (255, 75, 90), count=18, speed=4.0, size=4,
            )
            self.start_shake(5.0, 0.2)
            self._show_checkpoint_notice('O GUARDIÃO DO NÚCLEO DESPERTOU!')

    def _collect_power_up(self, power_up):
        if power_up.kind == 'health':
            self.player.health = min(
                self.player.max_health, self.player.health + 35
            )
            message = 'CURA +35'
        elif power_up.kind == 'rapid_fire':
            self.player.rapid_fire_timer = 8.0
            message = 'TIRO RÁPIDO!'
        else:
            self.player.invulnerability_timer = max(
                self.player.invulnerability_timer, 6.0
            )
            self.player.visible = True
            message = 'ESCUDO ATIVADO!'
        self._burst(
            power_up.center_x, power_up.center_y,
            (255, 220, 100), count=12, speed=3.0,
        )
        power_up.remove_from_sprite_lists()
        self._show_checkpoint_notice(message)
        audio.sfx('selecionar')

    def _activate_checkpoint(self, checkpoint):
        if checkpoint.activate():
            self.last_checkpoint = checkpoint
            self._burst(
                checkpoint.center_x, checkpoint.center_y,
                (120, 255, 170), count=14, speed=3.0,
            )
            self._show_checkpoint_notice('CHECKPOINT ATIVADO!')
            audio.sfx('selecionar')

    def _respawn_at_checkpoint(self):
        self.player.center_x = self.last_checkpoint.center_x
        self.player.center_y = (
            self.last_checkpoint.bottom + self.player.height / 2 + 2
        )
        self.player.change_x = 0
        self.player.change_y = 0
        self.player.health = self.player.max_health
        self.player.invulnerability_timer = 2.0
        self.player.hit_timer = 0
        self.player.visible = True
        self.player.jumps_used = 0
        self.projectiles = arcade.SpriteList()
        self.enemy_projectiles = arcade.SpriteList()
        self.camera.position = self._camera_position()

    def _spawn_static_coins(self):
        tentativas_max = 160
        geradas = 0
        tentativas = 0

        while geradas < TOTAL_STATIC_COINS and tentativas < tentativas_max:
            tentativas += 1
            coin = Coin('../sprites/Coin_tiles.png', COIN_SCALE, 1)
            coin.center_x = random.randint(50, int(self.world_width - 50))
            coin.center_y = random.randint(200, int(self.world_height - 50))

            if not arcade.check_for_collision_with_list(coin, self.blocos):
                self.coins.append(coin)
                geradas += 1

    def _spawn_special_coin(self):
        sc = SpecialCoin(scale=COIN_SCALE)
        sc.world_width = self.world_width
        sc.world_height = self.world_height
        sc.center_x = random.randint(100, int(self.world_width - 100))
        sc.center_y = random.randint(300, int(self.world_height - 100))
        self.special_coins.append(sc)

    def _spawn_enemies(self):
        if self.game_mode == 'hardcore':
            positions = [
                (
                    x,
                    VirtualGuy if index % 4 == 2
                    else PinkMan if index % 4 == 1 else Enemy,
                    1.6 if index % 4 == 2
                    else 1.2 if index % 4 == 1 else 2.0,
                )
                for index, x in enumerate(
                    range(700, int(self.world_width - 1400), 900)
                )
            ]
        else:
            positions = [
                (800, Enemy, 2.0), (400, PinkMan, 1.2),
                (1500, Enemy, 2.0), (2200, Enemy, 2.0),
            ]
            extra_positions = (2800, 3400, 4100)
            positions.extend(
                (x, Enemy, 2.0)
                for x in extra_positions[:self.enemy_wave]
            )
        for x, enemy_type, speed in positions:
            enemy = enemy_type(scale=2.0, speed=speed)
            enemy.center_x = x
            ground_tops = [
                bloco.top for bloco in self.blocos
                if abs(bloco.center_x - x) <= bloco.width / 2
                and bloco.top <= 160
            ]
            ground_top = max(ground_tops, default=self.world_height - 180)
            enemy.center_y = ground_top + enemy.height / 2 + 2
            self.enemies.append(enemy)
            self.enemy_physics.append(
                arcade.PhysicsEnginePlatformer(
                    enemy, walls=self.walls, gravity_constant=GRAVITY
                )
            )
            enemy.set_world_width(self.world_width)

    def _camera_position(self) -> tuple[float, float]:
        half_width = SCREEN_WIDTH / 2
        half_height = SCREEN_HEIGHT / 2
        return (
            max(half_width, min(self.player.center_x, self.world_width - half_width)),
            max(half_height, min(self.player.center_y, self.world_height - half_height)),
        )

    def start_shake(self, amplitude: float = 10.0, duration: float = 0.3):
        self.shake_amplitude = amplitude
        self.shake_duration = duration
        self.shake_time = duration

    def _burst(self, x, y, color, count=8, speed=3.0, size=4.0):
        create_burst(
            self.particles, x, y, color,
            count=count, speed=speed, size=size,
        )

    def _remove_expired_particles(self):
        for particle in list(self.particles):
            if particle.lifetime <= 0:
                particle.remove_from_sprite_lists()

    def _update_shake(self, delta_time: float):
        self.camera_center = self._camera_position()
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
        if key in (arcade.key.ESCAPE, arcade.key.P):
            self._toggle_pause()
            return
        if self.paused:
            if key == arcade.key.R:
                self._restart_game()
            elif key == arcade.key.M:
                self._return_to_menu()
            return

        self.keys_pressed.add(key)
        if key in (arcade.key.X, arcade.key.J):
            self._shoot()
        if key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player.jumps_used = 0
            if self.player.jumps_used < self.player.max_jumps:
                self.player.jump()
                self.player.jumps_used += 1
                self._burst(
                    self.player.center_x,
                    self.player.bottom,
                    (180, 235, 255),
                    count=6,
                    speed=2.2,
                    size=3,
                )
                audio.sfx('pulo')
    def on_mouse_press(self, x, y, button, modifiers):
        self.mouse_x = x
        self.mouse_y = y
        if self.paused:
            self._handle_pause_click(x, y)
            return
        if button == arcade.MOUSE_BUTTON_LEFT:
            self._shoot(x, y)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y
        if self.paused:
            for button in self.pause_buttons:
                button.active = button.contains(x, y)

    def _toggle_pause(self):
        self.paused = not self.paused
        self.keys_pressed.clear()

    def _restart_game(self):
        self.window.show_view(type(
            self
        )(self.player.name, self.window, self.game_mode))

    def _return_to_menu(self):
        from menu_view import MenuView
        self.window.show_view(MenuView(self.window))

    def _handle_pause_click(self, x, y):
        if self.pause_buttons[0].contains(x, y):
            self._toggle_pause()
        elif self.pause_buttons[1].contains(x, y):
            self._restart_game()
        elif self.pause_buttons[2].contains(x, y):
            self._return_to_menu()

    def _draw_pause_overlay(self):
        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH, 0, SCREEN_HEIGHT,
            (18, 24, 42, 170)
        )
        self.pause_panel.draw()
        self.pause_title.draw()
        for button in self.pause_buttons:
            button.draw()

    def _shoot(self, mouse_x=None, mouse_y=None):
        if not self.player.can_shoot():
            return
        if mouse_x is None:
            mouse_x = self.mouse_x
        if mouse_y is None:
            mouse_y = self.mouse_y
        camera_x, camera_y = self.camera.position
        target_x = camera_x + mouse_x - SCREEN_WIDTH / 2
        target_y = camera_y + mouse_y - SCREEN_HEIGHT / 2
        projectile = Projectile(
            self.player.center_x,
            self.player.center_y,
            target_x,
            target_y,
        )
        self.projectiles.append(projectile)
        self._burst(
            self.player.center_x, self.player.center_y,
            (255, 190, 60), count=4, speed=1.8, size=3,
        )

    def on_key_release(self, key, modifiers):
        self.keys_pressed.discard(key)
        self.player.on_key_release(key)

    def on_draw(self):
        crt_begin(self.window)
        self.clear()

        # mundo (treme junto com a câmera)
        with self.camera.activate():
            self.background.draw()
            self._draw_area_identity()
            self.blocos.draw()
            self.checkpoints.draw()
            self.power_ups.draw()
            if (
                self.boss_active
                and self.boss is not None
                and not self.boss.death_complete
            ):
                self.boss_list.draw()
                if self.boss.shielded:
                    arcade.draw_circle_outline(
                        self.boss.center_x, self.boss.center_y,
                        self.boss.width * 0.62, arcade.color.GOLD, 4
                    )
            self.enemies.draw()
            self.projectiles.draw()
            self.enemy_projectiles.draw()
            self.particles.draw()
            self.player_list.draw()
            self.coins.draw()
            self.special_coins.draw()

        # HUD (fixo, não treme)
        self.score_label.draw()
        self.timer_label.draw()

        if self.alert_timer > 0:
            self.alert_label.draw()
        if self.checkpoint_notice_timer > 0:
            self.checkpoint_notice_panel.draw()

        bar_left = SCREEN_WIDTH - 255
        bar_right = SCREEN_WIDTH - 35
        bar_bottom = SCREEN_HEIGHT - 44
        bar_top = SCREEN_HEIGHT - 16
        arcade.draw_lrbt_rectangle_filled(
            bar_left, bar_right, bar_bottom, bar_top,
            arcade.color.DARK_SLATE_GRAY
        )
        arcade.draw_lrbt_rectangle_outline(
            bar_left, bar_right, bar_bottom, bar_top,
            arcade.color.WHITE, 1
        )
        hp_width = 216 * max(0, self.player.health / self.player.max_health)
        arcade.draw_lrbt_rectangle_filled(
            bar_left + 2, bar_left + 2 + hp_width,
            bar_bottom + 2, bar_top - 2,
            arcade.color.GREEN if self.player.health > 40 else arcade.color.RED
        )
        arcade.draw_line(
            bar_left + 2, bar_top - 3,
            bar_left + 2 + hp_width, bar_top - 3,
            arcade.color.WHITE, 1
        )
        if (
            self.game_mode == 'hardcore'
            and self.boss_active
            and self.boss is not None
        ):
            boss_left = SCREEN_WIDTH / 2 - 260
            boss_right = SCREEN_WIDTH / 2 + 260
            boss_bottom = SCREEN_HEIGHT - 82
            boss_top = SCREEN_HEIGHT - 58
            arcade.draw_lrbt_rectangle_filled(
                boss_left, boss_right, boss_bottom, boss_top,
                arcade.color.DARK_SLATE_GRAY
            )
            arcade.draw_lrbt_rectangle_outline(
                boss_left, boss_right, boss_bottom, boss_top,
                arcade.color.WHITE, 2
            )
            boss_width = 516 * (
                self.boss.health / self.boss.max_health
            )
            arcade.draw_lrbt_rectangle_filled(
                boss_left + 2, boss_left + 2 + boss_width,
                boss_bottom + 2, boss_top - 2,
                arcade.color.RED_DEVIL
            )
            arcade.draw_text(
                'GUARDIÃO DO NÚCLEO',
                SCREEN_WIDTH / 2, boss_top + 7,
                arcade.color.WHITE, 14, anchor_x='center', bold=True
            )
        if self.paused:
            self._draw_pause_overlay()

        # O CRT precisa ser o último desenho para afetar também a pausa.
        draw_crt()

    def on_update(self, delta_time):
        if self.paused:
            return
        self.tempo += delta_time
        update_crt(delta_time)
        self._update_shake(delta_time)

        if self.alert_timer > 0:
            self.alert_timer -= delta_time
        if self.checkpoint_notice_timer > 0:
            self.checkpoint_notice_timer -= delta_time

        self.player_list.update(delta_time, self.keys_pressed)
        self.physics_engine.update()
        self.player.is_on_ground = self.physics_engine.can_jump()
        if self.player.is_on_ground:
            self.player.jumps_used = 0
        self._update_camera()

        defeated_enemies = []
        for i, enemy in enumerate(self.enemies):
            enemy.update(delta_time, player=self.player, walls=self.blocos)
            if (
                self.game_mode == 'hardcore'
                and isinstance(enemy, VirtualGuy)
                and enemy.can_shoot(self.player)
            ):
                x, y, target_x, target_y = enemy.shoot(self.player)
                self.enemy_projectiles.append(
                    EnemyProjectile(x, y, target_x, target_y)
                )
            if not enemy.defeated:
                previous_x = enemy.center_x
                self.enemy_physics[i].update()
            enemy.is_on_ground = self.enemy_physics[i].can_jump()
            if enemy.is_on_ground:
                enemy.jumps_remaining = 1
            if not enemy.defeated:
                enemy.handle_blocked(enemy.center_x - previous_x, delta_time)
            if enemy.defeated and enemy.hit_timer <= 0:
                defeated_enemies.append(i)

        for i in reversed(defeated_enemies):
            self.enemies[i].remove_from_sprite_lists()
            self.enemy_physics.pop(i)

        if not self.enemies:
            self.enemy_respawn_timer += delta_time
            if self.enemy_respawn_timer >= 2.0:
                self.enemy_wave = min(self.enemy_wave + 1, 3)
                self._spawn_enemies()
                self.enemy_respawn_timer = 0.0
        else:
            self.enemy_respawn_timer = 0.0

        self.coins.update(delta_time)
        self.special_coins.update(delta_time)
        self.projectiles.update(delta_time)
        self.enemy_projectiles.update(delta_time)
        self.particles.update(delta_time)
        self._remove_expired_particles()
        self.checkpoints.update(delta_time)
        self.power_ups.update(delta_time)
        if (
            self.boss_active
            and self.boss is not None
            and not self.boss.death_complete
        ):
            if not self.boss.defeated:
                self.boss.move_toward_player(
                    self.player, self.boss_arena_left, self.boss_arena_right
                )
            self.boss.update(delta_time)
            if not self.boss.defeated:
                self.boss_physics.update()
                self.boss.is_on_ground = self.boss_physics.can_jump()
            if self.boss.can_raise_shield():
                self.boss.raise_shield()
                self._burst(
                    self.boss.center_x, self.boss.center_y,
                    (255, 220, 70), count=16, speed=3.2,
                )
                self._show_checkpoint_notice('O NÚCLEO ESTÁ PROTEGIDO!')
            if self.boss.can_shoot():
                x, y, target_x, target_y = self.boss.shoot(self.player)
                self.enemy_projectiles.append(
                    EnemyProjectile(x, y, target_x, target_y)
                )
                if self.boss.attack_pattern == 1:
                    for offset in (-0.22, 0.22):
                        self.enemy_projectiles.append(
                            EnemyProjectile(
                                x, y, target_x + offset * 500, target_y
                            )
                        )
                elif self.boss.attack_pattern == 2:
                    for offset in (-180, 180):
                        self.enemy_projectiles.append(
                            EnemyProjectile(
                                x, y, target_x, target_y + offset
                            )
                        )
            if self.boss.melee_hit(self.player):
                if self.player.receive_damage(2):
                    self.player.apply_knockback(self.boss.center_x, 12, 10)
                    self.start_shake(10.0, 0.25)
                    audio.sfx('dano')

        if self.game_mode == 'hardcore':
            self._update_boss_activation()
            for checkpoint in self.checkpoints:
                if (
                    not checkpoint.active
                    and arcade.check_for_collision(self.player, checkpoint)
                ):
                    self._activate_checkpoint(checkpoint)
            for power_up in arcade.check_for_collision_with_list(
                self.player, self.power_ups
            ):
                self._collect_power_up(power_up)

        for projectile in list(self.projectiles):
            if projectile.right < 0 or projectile.left > self.world_width:
                projectile.remove_from_sprite_lists()
                continue
            if arcade.check_for_collision_with_list(projectile, self.walls):
                self._burst(
                    projectile.center_x, projectile.center_y,
                    (255, 210, 80), count=5, speed=2.0, size=3,
                )
                projectile.remove_from_sprite_lists()
                continue
            for enemy in arcade.check_for_collision_with_list(projectile, self.enemies):
                if not enemy.defeated:
                    direction = 1 if projectile.change_x >= 0 else -1
                    enemy.receive_hit(1, direction)
                    self._burst(
                        enemy.center_x, enemy.center_y,
                        (255, 100, 100), count=9, speed=3.0,
                    )
                    self.player.score += 10
                    audio.sfx('mosca')
                projectile.remove_from_sprite_lists()
                break
            if (
                self.boss_active
                and self.boss is not None
                and not self.boss.defeated
                and arcade.check_for_collision(projectile, self.boss)
            ):
                self.boss.receive_hit()
                self._burst(
                    self.boss.center_x, self.boss.center_y,
                    (255, 70, 90), count=12, speed=3.5,
                )
                self.start_shake(4.0, 0.12)
                self.player.score += 25
                projectile.remove_from_sprite_lists()

        for projectile in list(self.enemy_projectiles):
            if (
                projectile.right < 0
                or projectile.left > self.world_width
                or projectile.top < 0
                or projectile.bottom > self.world_height
            ):
                projectile.remove_from_sprite_lists()
                continue
            if arcade.check_for_collision_with_list(projectile, self.walls):
                self._burst(
                    projectile.center_x, projectile.center_y,
                    (120, 210, 255), count=5, speed=2.0, size=3,
                )
                projectile.remove_from_sprite_lists()
                continue
            if arcade.check_for_collision(projectile, self.player):
                if self.player.receive_damage(projectile.damage):
                    self._burst(
                        self.player.center_x, self.player.center_y,
                        (255, 75, 75), count=10, speed=3.2,
                    )
                    self.start_shake(5.0, 0.15)
                    audio.sfx('dano')
                    crt_glitch(0.7, 0.2)
                    self.alert_label.text = '- 1 PONTO!'
                    self.alert_timer = 1.0
                projectile.remove_from_sprite_lists()

        for coin in arcade.check_for_collision_with_list(self.player, self.coins):
            self.player.score += coin.value
            self.collected_coins += 1
            self._burst(
                coin.center_x, coin.center_y,
                (255, 220, 80), count=8, speed=2.5, size=3,
            )
            audio.sfx('mosca')
            coin.remove_from_sprite_lists()

        for sc in arcade.check_for_collision_with_list(self.player, self.special_coins):
            self.player.score += sc.value
            self._burst(
                sc.center_x, sc.center_y,
                (220, 120, 255), count=12, speed=3.0,
            )
            sc.remove_from_sprite_lists()
            audio.sfx('mosca_especial')
            self._spawn_special_coin()

        for enemy in arcade.check_for_collision_with_list(self.player, self.enemies):
            enemy_x = enemy.center_x  # antes do on_hit_player (PinkMan teleporta)
            if enemy.on_hit_player(self.player):
                self._burst(
                    self.player.center_x, self.player.center_y,
                    (255, 75, 75), count=10, speed=3.0,
                )
                self.player.apply_knockback(enemy_x)
                self.start_shake()
                audio.sfx('dano')
                crt_glitch(1.0, 0.35)
                self.alert_label.text = '- 1 PONTO!'
                self.alert_timer = 1.0

        if self.player.health <= 0:
            if self.game_mode == 'hardcore' and self.last_checkpoint is not None:
                self._respawn_at_checkpoint()
                self._show_checkpoint_notice('VOCÊ VOLTOU AO CHECKPOINT!')
                self.start_shake(6.0, 0.2)
                return
            from game_over_view import GameOverView
            audio.parar_musica()
            set_default_cursor(self.window)
            self.window.show_view(GameOverView(
                score=self.player.score,
                max_score=TOTAL_STATIC_COINS,
                tempo=self.tempo,
                nome=self.player.name,
                modo=self.game_mode,
                venceu=False,
            ))
            return

        self.score_label.text = f'Score: {self.player.score}'
        self.timer_label.text = f'Tempo: {self.tempo:.1f}s'

        venceu = (
            self.boss is not None and self.boss.death_complete
            if self.game_mode == 'hardcore'
            else self.collected_coins >= TOTAL_STATIC_COINS
            and len(self.coins) == 0
        )
        if (
            self.game_mode == 'hardcore'
            and self.boss is not None
            and self.boss.death_complete
            and not self.boss_rewarded
        ):
            self.player.score += 500
            self.boss_rewarded = True
            self._show_checkpoint_notice('BOSS DERROTADO! +500 PONTOS')
        if venceu:
            from game_over_view import GameOverView
            audio.parar_musica()
            audio.sfx('vitoria')
            set_default_cursor(self.window)
            self.window.show_view(GameOverView(
                score=self.player.score,
                max_score=TOTAL_STATIC_COINS,
                tempo=self.tempo,
                nome=self.player.name,
                modo=self.game_mode,
            ))

    def _update_camera(self):
        """Mantém a câmera centrada no jogador sem revelar fora do mapa."""
        self.camera_center = self._camera_position()
        if self.shake_time <= 0:
            self.camera.position = self.camera_center

    def on_hide_view(self):
        set_default_cursor(self.window)