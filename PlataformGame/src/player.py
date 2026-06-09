from entity import Entity
from constants import PLAYER_JUMP_SPEED
import arcade

class Player(Entity):
    def __init__(self, sprite: str, scale : float, speed: float, max_health: int):
        super().__init__(sprite, scale, speed, max_health)
        self.facing_right = True
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_speed = 0.1

        self.idle_textures = self.load_atlas('../sprites/Frog/frog_idle.png', 4)
        self.run_textures = self.load_atlas('../sprites/Frog/frog_run.png', 6)
        self.jump_textures = self.load_atlas('../sprites/Frog/frog_jump.png', 1)
        self.fall_textures = self.load_atlas('../sprites/Frog/frog_fall.png', 1)
        self.current_textures = self.idle_textures

        self.jump_speed = PLAYER_JUMP_SPEED
        self.score = 0
        self.is_on_ground = False
    
    def update(self, delta_time : float = 1/60, keys: set = None):
        if keys is None:
            keys = set()
        if arcade.key.LEFT in keys or arcade.key.A in keys:
            self.change_x = -self.speed 
        elif arcade.key.RIGHT in keys or arcade.key.D in keys:
            self.change_x = self.speed 
        else: 
            self.change_x = 0
        
        if self.change_y > 0:
            new_textures = self.jump_textures
        elif self.change_y < 0:
            new_textures = self.fall_textures
        elif self.change_x != 0:
            new_textures = self.run_textures
        else:
            new_textures = self.idle_textures

        if new_textures is not self.current_textures:
            self.current_textures = new_textures
            self.current_frame = 0

        if self.change_x > 0:
            self.facing_right = True
        elif self.change_x < 0:
            self.facing_right = False

        self.frame_timer += delta_time
        if self.frame_timer >= self.frame_speed:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.current_textures)

        direction = 0 if self.facing_right else 1
        self.texture = self.current_textures[self.current_frame][direction]
    
    def load_atlas(self, path, frame_count):
        sheet = arcade.texture.spritesheet.SpriteSheet(path)
        textures = []
        for i in range(frame_count):
            rect = arcade.LRBT(
                left=i * 32,
                right=i * 32 + 32,
                bottom=0,
                top=32
            )
            tex_right = sheet.get_texture(rect)
            sheet.flip_left_right()
            tex_left = sheet.get_texture(rect)
            sheet.flip_left_right()
            textures.append((tex_right, tex_left))
        return textures

    def on_key_press(self, key):
        if key == arcade.key.SPACE:
            self.jump()
    
    def on_key_release(self, key):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.change_x = 0

    def jump(self):
        if self.is_on_ground:
            self.change_y = self.jump_speed
            self.is_on_ground = False