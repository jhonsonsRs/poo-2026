from player import Player
from coin import Coin
from constants import SCREEN_WIDTH, PLAYER_MAX_HEALTH, PLAYER_SCALE, PLAYER_SPEED, TILE_SCALE, TILE_SIZE, GRAVITY, COIN_SCALE
import arcade

class GameView(arcade.View):
    def __init__(self, window = None):
        super().__init__(window)
        self.keys_pressed = set()
        self.player = Player('../sprites/Frog/frog.png', PLAYER_SCALE, PLAYER_SPEED, PLAYER_MAX_HEALTH)
        self.player.center_x = 400
        self.player.center_y = 300
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
        self.coin = Coin('../sprites/Coin_tiles.png', COIN_SCALE, 1)
        self.coin.center_x = 500
        self.coin.center_y = 200
        self.coins = arcade.SpriteList()
        self.coins.append(self.coin)
        self.static_objects = arcade.SpriteList()
        for x in range(0, SCREEN_WIDTH + int(TILE_SIZE * TILE_SCALE), int(TILE_SIZE * TILE_SCALE)):
            ground = arcade.SpriteSolidColor(TILE_SIZE, TILE_SIZE, color=arcade.color.WHITE)
            ground.scale = TILE_SCALE
            ground.center_x = x
            ground.center_y = TILE_SIZE * TILE_SCALE / 2
            self.static_objects.append(ground)
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            walls=self.static_objects,
            gravity_constant=GRAVITY
        )
    
    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        self.player.on_key_press(key)

    def on_key_release(self, key, modifiers):
        self.keys_pressed.discard(key)
        self.player.on_key_release(key)

    def on_draw(self):
        self.clear()
        self.player_list.draw()
        self.static_objects.draw()
        self.coins.draw()

    def on_update(self, delta_time):
        self.player_list.update(delta_time, self.keys_pressed)
        self.coins.update(delta_time)
        self.physics_engine.update()
        self.player.is_on_ground = self.physics_engine.can_jump()
        coins_hit = arcade.check_for_collision_with_list(self.player, self.coins)
        for coin in coins_hit:
            self.player.score += coin.value
            coin.remove_from_sprite_lists()
        