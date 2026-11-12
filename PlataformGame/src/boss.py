import arcade
import math


class Boss(arcade.Sprite):
    FRAME_SIZE = (64, 80)

    def __init__(self, x: float, y: float):
        self.idle_frames = self._load_frames('../sprites/Boss/boss_idle.png', 6)
        self.attack_frames = self._load_frames(
            '../sprites/Boss/boss_attack.png', 5
        )
        self.hit_frames = self._load_frames('../sprites/Boss/boss_hit.png', 3)
        self.death_frames = self._load_frames(
            '../sprites/Boss/boss_death.png', 6
        )
        super().__init__(self.idle_frames[0], 2.0)
        self.center_x = x
        self.center_y = y
        self.max_health = 30
        self.health = self.max_health
        self.defeated = False
        self.hit_timer = 0.0
        self.shoot_timer = 1.2
        self.summon_timer = 0.0
        self.animation_timer = 0.0
        self.animation_frame = 0
        self.animation_state = 'idle'
        self._phase = 1
        self.is_on_ground = False
        self.death_timer = 0.0
        self.shielded = False
        self.shield_timer = 0.0
        self.shield_cooldown = 4.0
        self.attack_pattern = 0

    def _load_frames(self, path: str, count: int):
        sheet = arcade.texture.spritesheet.SpriteSheet(path)
        return [
            sheet.get_texture(
                arcade.LRBT(
                    index * self.FRAME_SIZE[0],
                    (index + 1) * self.FRAME_SIZE[0],
                    0,
                    self.FRAME_SIZE[1],
                )
            )
            for index in range(count)
        ]

    @property
    def phase(self):
        if self.health <= self.max_health * 0.33:
            return 3
        if self.health <= self.max_health * 0.66:
            return 2
        return 1

    def update(self, delta_time: float = 1 / 60):
        self.shoot_timer = max(0, self.shoot_timer - delta_time)
        self.summon_timer = max(0, self.summon_timer - delta_time)
        self.shield_cooldown = max(0, self.shield_cooldown - delta_time)
        if self.shield_timer > 0:
            self.shield_timer = max(0, self.shield_timer - delta_time)
        self.shielded = self.shield_timer > 0
        if self.hit_timer > 0:
            self.hit_timer = max(0, self.hit_timer - delta_time)
        if self.defeated:
            frames = self.death_frames
            self.animation_state = 'death'
        elif self.hit_timer > 0:
            frames = self.hit_frames
            self.animation_state = 'hit'
        elif self.animation_state == 'attack':
            frames = self.attack_frames
        else:
            frames = self.idle_frames
            self.animation_state = 'idle'
        self.animation_timer += delta_time
        if self.animation_timer >= 0.1:
            self.animation_timer = 0
            self.animation_frame = min(
                self.animation_frame + 1, len(frames) - 1
            )
        self.texture = frames[self.animation_frame]
        if self.defeated:
            self.death_timer += delta_time

    def can_shoot(self):
        return (
            not self.defeated
            and not self.shielded
            and self.shoot_timer <= 0
        )

    def shoot(self, player):
        self.shoot_timer = 1.7 if self.phase == 1 else 1.2
        if self.phase == 3:
            self.shoot_timer = 0.85
        self.attack_pattern = (self.attack_pattern + 1) % 3
        self.animation_state = 'attack'
        self.animation_frame = 0
        self.animation_timer = 0
        return (
            self.center_x,
            self.center_y,
            player.center_x,
            player.center_y,
        )

    def receive_hit(self, damage: int = 1):
        if self.defeated or self.shielded:
            return
        self.health -= damage
        self.hit_timer = 0.16
        self.animation_state = 'hit'
        self.animation_frame = 0
        self.animation_timer = 0
        if self.health <= 0:
            self.health = 0
            self.defeated = True
            self.death_timer = 0.0

    def move_toward_player(self, player, left_limit: float, right_limit: float):
        if self.defeated or self.shielded:
            self.change_x = 0
            return
        distance = player.center_x - self.center_x
        if abs(distance) > 360:
            self.change_x = 1.4 if distance > 0 else -1.4
        else:
            self.change_x = 0
        self.center_x = max(
            left_limit + self.width / 2,
            min(self.center_x, right_limit - self.width / 2),
        )

    def can_raise_shield(self):
        return (
            not self.defeated
            and self.phase == 2
            and not self.shielded
            and self.shield_cooldown <= 0
        )

    def raise_shield(self):
        self.shielded = True
        self.shield_timer = 2.5
        self.shield_cooldown = 7.0

    def melee_hit(self, player) -> bool:
        if self.defeated or self.shielded:
            return False
        return abs(player.center_x - self.center_x) < 150

    @property
    def death_complete(self):
        return self.defeated and self.death_timer >= 0.7
