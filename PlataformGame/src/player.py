from entity import Entity
from constants import PLAYER_JUMP_SPEED
import arcade

class Player(Entity):
    def __init__(self, sprite: str, scale : float, speed: float, max_health: int):
        super().__init__(sprite, scale, speed, max_health)
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