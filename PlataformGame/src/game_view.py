from player import Player
import arcade

class GameView(arcade.View):
    def __init__(self, window = None):
        super().__init__(window)
        self.player = Player('../sprites/frog.png', 1.0, 15.0, 100)
        self.player.center_x = 400
        self.player.center_y = 300

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
    
    def on_draw(self):
        self.clear()
        self.player_list.draw()

    def on_update(self, delta_time):
        self.player_list.update()