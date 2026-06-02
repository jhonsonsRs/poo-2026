from entity import Entity
import arcade

class Player(Entity):
    def __init__(self, sprite: str, scale : float, speed: float, max_health: int):
        super().__init__(sprite, scale, speed, max_health)
        self.jump_speed = 15.0
        self.score = 0
        self.is_on_ground = False
    
    def update(self, delta_time : float = 1/60):
        keys = arcade.get_keys_pressed()
        if arcade.key.LEFT in arcade.key.A in keys:
            self.change_x = -self.speed
        elif arcade.key.RIGHT in arcade.key.D in keys:
            self.change_x = self.speed
        else: 
            self.change_x = 0
    
    def jump(self):
        if self.is_on_ground:
            self.change_y = +self.jump_speed
            self.is_on_ground = False

    