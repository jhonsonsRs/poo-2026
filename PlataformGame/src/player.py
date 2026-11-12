import arcade
from entity import Entity
from constants import PLAYER_JUMP_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT

LARGURA_QUADRO = 32
ALTURA_QUADRO = 32
INTERVALO_QUADRO = 0.1  # troca de quadro da caminhada a cada 100 ms


class Player(Entity):
    def __init__(self, sprite: str, scale: float, speed: float, max_health: int, name: str):
        super().__init__(sprite, scale, speed, max_health)
        self.virado_para = 'direita'   # 'direita' ou 'esquerda'
        self.frame_atual = 0
        self.frame_timer = 0.0
        self.estado = 'parado'

        self.name = name
        self.idle_textures = self.carregar_quadros('../sprites/Frog/frog_idle.png', 4)
        self.walk_textures = self.carregar_quadros('../sprites/Frog/frog_run.png',  6)
        self.jump_textures = self.carregar_quadros('../sprites/Frog/frog_jump.png', 1)
        self.fall_textures = self.carregar_quadros('../sprites/Frog/frog_fall.png', 1)
        self.hit_textures = self.carregar_quadros('../sprites/Frog/frog_hit.png', 7)

        self.jump_speed = PLAYER_JUMP_SPEED
        self.score = 0
        self.is_on_ground = False
        self.knockback_timer = 0.0
        self.jumps_used = 0
        self.max_jumps = 2
        self.shoot_cooldown = 0.0
        self.hit_timer = 0.0
        self.invulnerability_timer = 0.0
        self.rapid_fire_timer = 0.0
        self._blink_timer = 0.0
        self.world_width = SCREEN_WIDTH
        self.world_height = SCREEN_HEIGHT

    def set_world_bounds(self, width: float, height: float):
        self.world_width = width
        self.world_height = height

    def carregar_quadros(self, caminho: str, quantidade: int) -> dict:
        """Fatia a folha de sprites e devolve os quadros virados p/ direita e esquerda."""
        folha = arcade.load_spritesheet(caminho)
        direita = folha.get_texture_grid(
            size=(LARGURA_QUADRO, ALTURA_QUADRO),
            columns=quantidade,
            count=quantidade,
        )
        esquerda = [textura.flip_left_right() for textura in direita]
        return {'direita': direita, 'esquerda': esquerda}

    def update(self, delta_time: float = 1/60, keys: set = None):
        if keys is None:
            keys = set()

        em_knockback = self.knockback_timer > 0
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= delta_time
        if self.rapid_fire_timer > 0:
            self.rapid_fire_timer = max(0, self.rapid_fire_timer - delta_time)
        if self.hit_timer > 0:
            self.hit_timer -= delta_time
        if self.invulnerability_timer > 0:
            self.invulnerability_timer = max(0, self.invulnerability_timer - delta_time)
            if self.invulnerability_timer > 0:
                self._blink_timer += delta_time
                self.visible = int(self._blink_timer / 0.08) % 2 == 0
            else:
                self.visible = True
        else:
            self.visible = True
        if em_knockback:
            self.knockback_timer -= delta_time
        else:
            if arcade.key.LEFT in keys or arcade.key.A in keys:
                self.change_x = -self.speed
            elif arcade.key.RIGHT in keys or arcade.key.D in keys:
                self.change_x = self.speed
            else:
                self.change_x = 0

        self.center_x = max(self.width / 2, min(self.center_x, self.world_width - self.width / 2))
        self.center_y = max(self.height / 2, min(self.center_y, self.world_height - self.height / 2))

        if not em_knockback:
            if self.change_x > 0:
                self.virado_para = 'direita'
            elif self.change_x < 0:
                self.virado_para = 'esquerda'

        self._atualizar_animacao(delta_time)

    def _atualizar_animacao(self, delta_time: float):
        """Máquina de estados. Prioridade: pulo/queda -> parado -> andando."""
        if self.hit_timer > 0:
            novo_estado = 'atingido'
        elif self.change_y != 0:
            novo_estado = 'pulo' if self.change_y > 0 else 'queda'
        elif self.change_x == 0:
            novo_estado = 'parado'
        else:
            novo_estado = 'andando'

        if novo_estado != self.estado:
            self.estado = novo_estado
            self.frame_atual = 0
            self.frame_timer = 0.0

        if self.estado == 'atingido':
            quadros = self.hit_textures[self.virado_para]
            self.frame_timer += delta_time
            while self.frame_timer >= INTERVALO_QUADRO:
                self.frame_timer -= INTERVALO_QUADRO
                self.frame_atual = min(self.frame_atual + 1, len(quadros) - 1)
        elif self.estado == 'pulo':
            quadros = self.jump_textures[self.virado_para]
        elif self.estado == 'queda':
            quadros = self.fall_textures[self.virado_para]
        elif self.estado == 'parado':
            quadros = self.idle_textures[self.virado_para]
            self.frame_atual = 0          # textura estática
        else:
            quadros = self.walk_textures[self.virado_para]
            self.frame_timer += delta_time
            while self.frame_timer >= INTERVALO_QUADRO:
                self.frame_timer -= INTERVALO_QUADRO
                self.frame_atual = (self.frame_atual + 1) % len(quadros)

        self.texture = quadros[self.frame_atual]

    def on_key_release(self, key):
        if self.knockback_timer > 0:
            return
        if key in (arcade.key.LEFT, arcade.key.A):
            self.change_x = 0
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.change_x = 0

    def jump(self):
        """Aplica o impulso. Quem decide se pode pular é o can_jump() da física."""
        self.change_y = self.jump_speed
        self.is_on_ground = False

    def can_shoot(self) -> bool:
        if self.shoot_cooldown > 0 or self.hit_timer > 0:
            return False
        self.shoot_cooldown = 0.25
        if self.rapid_fire_timer > 0:
            self.shoot_cooldown = 0.08
        return True

    def receive_damage(self, damage: int) -> bool:
        if self.invulnerability_timer > 0:
            return False
        self.take_damage(damage)
        self.hit_timer = 0.35
        self.invulnerability_timer = 1.1
        self._blink_timer = 0.0
        self.visible = True
        self.frame_atual = 0
        self.frame_timer = 0.0
        return True

    def apply_knockback(self, source_x: float, force_x: float = 9.0,
                        force_y: float = 8.0, duration: float = 0.2):
        direction = 1 if self.center_x >= source_x else -1
        self.change_x = direction * force_x
        self.change_y = force_y
        self.knockback_timer = duration
        self.is_on_ground = False
