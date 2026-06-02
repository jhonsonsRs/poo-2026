from entity import Entity
import arcade

class Enemy(Entity):
    def __init__(self, sprite, scale, speed, max_health):
        super().__init__(sprite, scale, speed, max_health)
        self.damage = 10
    