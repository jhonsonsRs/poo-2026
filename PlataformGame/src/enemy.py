import arcade
import random
from entity import Entity
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Enemy(Entity):
    SPRITE_SIZE = 32

    def __init__(self, scale: float = 2.0, speed: float = 2.0, max_health: int = 999):
        super().__init__(None, scale, speed, 3)

        self.facing_right = True
        self.current_frame = 0
        self.frame_timer = 0.0
        self.frame_speed = 0.08

        self.idle_textures = self._load_atlas('../sprites/Ninja/ninja_idle.png', 11)
        self.run_textures  = self._load_atlas('../sprites/Ninja/ninja_run.png',  12)
        self.jump_textures = self._load_atlas('../sprites/Ninja/ninja_jump.png',  1)
        self.fall_textures = self._load_atlas('../sprites/Ninja/ninja_fall.png',  1)
        self.hit_textures = self._load_atlas('../sprites/Ninja/Hit (32x32).png', 7)
        self.current_textures = self.idle_textures

        self.damage = 1
        self.hit_cooldown = 0.0
        self.is_on_ground = False
        self.jump_speed = 12.0
        self.jumps_remaining = 1
        self.jump_cooldown = 0.0
        self.detection_range = 700.0
        self.stop_distance = 24.0
        self.patrol_direction = 1
        self.hit_timer = 0.0
        self.defeated = False
        self.stuck_timer = 0.0
        self.last_x = self.center_x
        self.world_width = None

        self._edge_sensor = arcade.SpriteSolidColor(4, 8, arcade.color.RED)
        self._front_sensor = arcade.SpriteSolidColor(8, 42, arcade.color.RED)

        self.center_x = random.randint(100, SCREEN_WIDTH - 100)
        self.center_y = 400
        self.texture = self.idle_textures[0][0]

    def set_world_width(self, width: float):
        self.world_width = width

    def _load_atlas(self, path: str, frame_count: int):
        sheet = arcade.texture.spritesheet.SpriteSheet(path)
        textures = []
        s = self.SPRITE_SIZE
        for i in range(frame_count):
            rect = arcade.LRBT(i * s, i * s + s, 0, s)
            tex_r = sheet.get_texture(rect)
            sheet.flip_left_right()
            tex_l = sheet.get_texture(rect)
            sheet.flip_left_right()
            textures.append((tex_r, tex_l))
        return textures

    def _update_edge_sensor(self):
        offset = (self.width / 2 + 4) * (1 if self.facing_right else -1)
        self._edge_sensor.center_x = self.center_x + offset
        self._edge_sensor.center_y = self.bottom - 4

    def _should_jump(self, walls):
        self._update_edge_sensor()
        hits = arcade.check_for_collision_with_list(self._edge_sensor, walls)
        return len(hits) == 0

    def _blocked_ahead(self, walls):
        offset = self.width / 2 + 5
        self._front_sensor.center_x = self.center_x + (
            offset if self.facing_right else -offset
        )
        self._front_sensor.center_y = self.center_y + 4
        return bool(arcade.check_for_collision_with_list(self._front_sensor, walls))

    def _chase(self, player):
        distance_x = player.center_x - self.center_x
        if abs(distance_x) > self.detection_range:
            self.change_x = self.speed * self.patrol_direction * 0.5
            self.facing_right = self.change_x > 0
        elif distance_x > self.stop_distance:
            self.change_x = self.speed
            self.facing_right = True
        elif distance_x < -self.stop_distance:
            self.change_x = -self.speed
            self.facing_right = False
        else:
            self.change_x = 0

    def jump(self):
        if self.is_on_ground and self.jumps_remaining > 0:
            self.change_y = self.jump_speed
            self.is_on_ground = False
            self.jumps_remaining -= 1

    def update(self, delta_time: float = 1/60, player=None, walls=None):
        if self.hit_cooldown > 0:
            self.hit_cooldown -= delta_time
        if self.jump_cooldown > 0:
            self.jump_cooldown -= delta_time
        if self.hit_timer > 0:
            self.hit_timer -= delta_time
        if abs(self.center_x - self.last_x) < 0.1 and abs(self.change_x) > 0:
            self.stuck_timer += delta_time
        else:
            self.stuck_timer = 0.0
        self.last_x = self.center_x

        if self.defeated:
            self._animate(delta_time)
            return

        if self.world_width is not None:
            self.center_x = max(
                self.width / 2,
                min(self.center_x, self.world_width - self.width / 2),
            )

        if player:
            self._chase(player)

            blocked = walls and self.is_on_ground and self._blocked_ahead(walls)
            at_edge = walls and self.is_on_ground and self._should_jump(walls)
            outside_detection = abs(player.center_x - self.center_x) > self.detection_range
            if blocked and self.jump_cooldown <= 0:
                self.jump()
                self.jump_cooldown = 0.6
            elif at_edge and outside_detection:
                self.patrol_direction *= -1
                self.change_x = self.speed * self.patrol_direction * 0.5
                self.facing_right = self.change_x > 0
            elif at_edge and self.jump_cooldown <= 0:
                self.jump()
                self.jump_cooldown = 0.6

            if (
                self.is_on_ground
                and self.jump_cooldown <= 0
                and player.center_y > self.center_y + 55
                and abs(player.center_x - self.center_x) < self.detection_range
            ):
                self.jump()
                self.jump_cooldown = 0.6

            if self.stuck_timer > 0.25 and self.is_on_ground:
                self.jump()
                self.jump_cooldown = 0.6

        self._animate(delta_time)

    def _animate(self, delta_time):
        if self.hit_timer > 0:
            new_tex = self.hit_textures
        elif self.change_y > 0:
            new_tex = self.jump_textures
        elif self.change_y < 0:
            new_tex = self.fall_textures
        elif self.change_x != 0:
            new_tex = self.run_textures
        else:
            new_tex = self.idle_textures

        if new_tex is not self.current_textures:
            self.current_textures = new_tex
            self.current_frame = 0

        self.frame_timer += delta_time
        if self.frame_timer >= self.frame_speed:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.current_textures)

        direction = 0 if self.facing_right else 1
        self.texture = self.current_textures[self.current_frame][direction]

    def receive_hit(self, damage: int, direction: int):
        if self.defeated:
            return False
        self.take_damage(damage)
        self.hit_timer = 0.35
        self.current_frame = 0
        self.frame_timer = 0.0
        self.change_x = direction * 3.0
        if self.is_dead():
            self.defeated = True
            self.change_x = 0
            self.change_y = 0
        return True

    def handle_blocked(self, moved: float, delta_time: float):
        if self.defeated or not self.is_on_ground or abs(self.change_x) < 0.1:
            return
        if abs(moved) < 0.05:
            self.stuck_timer += delta_time
            self.change_x = 0
            if self.stuck_timer > 0.2:
                self.patrol_direction *= -1
                self.facing_right = self.patrol_direction > 0
                self.change_x = self.speed * self.patrol_direction
                self.stuck_timer = 0
        else:
            self.stuck_timer = 0

    def on_hit_player(self, player) -> bool:
        if not self.defeated and self.hit_cooldown <= 0:
            if not player.receive_damage(self.damage):
                return False
            self.hit_cooldown = 1.0
            return True
        return False


class PinkMan(Enemy):
    def __init__(self, scale: float = 2.0, speed: float = 1.2, max_health: int = 999):
        super().__init__(scale, speed, max_health)

        self.idle_textures = self._load_atlas('../sprites/PinkMan/pinkman_idle.png', 11)
        self.run_textures  = self._load_atlas('../sprites/PinkMan/pinkman_run.png',  12)
        self.jump_textures = self._load_atlas('../sprites/PinkMan/pinkman_jump.png',  1)
        self.fall_textures = self._load_atlas('../sprites/PinkMan/pinkman_fall.png',  1)
        self.hit_textures = self._load_atlas('../sprites/PinkMan/Hit (32x32).png', 7)
        self.current_textures = self.idle_textures
        self.texture = self.idle_textures[0][0]

    def _teleport(self):
        limit = self.world_width or SCREEN_WIDTH
        self.center_x = random.randint(100, int(limit - 100))
        self.center_y = 400
        self.change_x = 0
        self.change_y = 0

    def on_hit_player(self, player) -> bool:
        if self.hit_cooldown <= 0:
            if not player.receive_damage(self.damage):
                return False
            self._teleport()
            self.hit_cooldown = 0.5
            return True
        return False


class VirtualGuy(Enemy):
    """Enemy that keeps distance and periodically shoots at the player."""

    def __init__(self, scale: float = 2.0, speed: float = 1.6,
                 max_health: int = 999):
        super().__init__(scale, speed, max_health)
        base = '../sprites/Virtual Guy/'
        self.idle_textures = self._load_atlas(base + 'Idle (32x32).png', 11)
        self.run_textures = self._load_atlas(base + 'Run (32x32).png', 12)
        self.jump_textures = self._load_atlas(base + 'Jump (32x32).png', 1)
        self.fall_textures = self._load_atlas(base + 'Fall (32x32).png', 1)
        self.hit_textures = self._load_atlas(base + 'Hit (32x32).png', 7)
        self.current_textures = self.idle_textures
        self.texture = self.idle_textures[0][0]
        self.stop_distance = 280.0
        self.detection_range = 950.0
        self.shoot_timer = 1.0
        self.shoot_interval = 1.8

    def _chase(self, player):
        distance_x = player.center_x - self.center_x
        if abs(distance_x) > self.detection_range:
            self.change_x = 0
        elif distance_x > self.stop_distance:
            self.change_x = self.speed
            self.facing_right = True
        elif distance_x < -self.stop_distance:
            self.change_x = -self.speed
            self.facing_right = False
        else:
            self.change_x = 0

    def update(self, delta_time: float = 1 / 60, player=None, walls=None):
        self.shoot_timer = max(0, self.shoot_timer - delta_time)
        super().update(delta_time, player, walls)

    def can_shoot(self, player) -> bool:
        return (
            not self.defeated
            and self.shoot_timer <= 0
            and abs(player.center_x - self.center_x) <= self.detection_range
        )

    def shoot(self, player):
        self.shoot_timer = self.shoot_interval
        return (
            self.center_x,
            self.center_y + self.height * 0.15,
            player.center_x,
            player.center_y,
        )