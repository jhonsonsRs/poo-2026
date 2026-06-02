import arcade
class Entity(arcade.Sprite):
    def __init__(self, sprite, scale, speed, max_health):
        super().__init__(sprite, scale)
        self.speed = speed
        self.max_health = max_health
        self.health = max_health
    
    def update(self, delta_time):
        pass

    def take_damage(self, damage: int):
        self.health -= damage
    
    def is_dead(self) -> bool:
        if self.health <= 0:
            return True
        return False