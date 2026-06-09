from player import Player
from coin import Coin
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_MAX_HEALTH, PLAYER_SCALE, PLAYER_SPEED, TILE_SCALE, TILE_SIZE, GRAVITY, COIN_SCALE
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
        self.coin.center_x = 20 * 16 * 2
        self.coin.center_y = (25 * 16 * 2) - (16 * 16 * 2)
        self.coin_2 = Coin('../sprites/Coin_tiles.png', COIN_SCALE, 1)
        self.coin_2.center_x = 32 * 16 * 2
        self.coin_2.center_y = (25*16*2) - (12*16*2)
        self.coin_3 = Coin('../sprites/Coin_tiles.png', COIN_SCALE, 1)
        self.coin_3.center_x = 9 * 16 * 2
        self.coin_3.center_y = (25*16*2) - (12*16*2)
        self.coin_4 = Coin('../sprites/Coin_tiles.png', COIN_SCALE, 1)
        self.coin_4.center_x = 20 * 16 * 2
        self.coin_4.center_y = (25*16*2) - (6*16*2)
        self.spawn_coins()
        self.tile_map = arcade.load_tilemap('../sprites/map/level_1.tmx', scaling=2.0)
        self.static_objects = self.tile_map.sprite_lists['Plataforms']
        self.background = self.tile_map.sprite_lists['Background']
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            walls=self.static_objects,
            gravity_constant=GRAVITY
        )
        self.score_label = arcade.Text(
            text='Score: 0',
            x=10,
            y=SCREEN_HEIGHT - 30,
            color=arcade.color.RED_DEVIL,
            font_size=16,
            bold=True
        )
    
    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        self.player.on_key_press(key)
        if key == arcade.key.R:
            #if len(self.coins) >= 3:
            #    return
            self.spawn_coins()

    def on_key_release(self, key, modifiers):
        self.keys_pressed.discard(key)
        self.player.on_key_release(key)

    def on_draw(self):
        self.clear()
        self.background.draw()
        self.static_objects.draw()
        self.player_list.draw()
        self.coins.draw()
        self.score_label.draw()
        arcade.draw_lrbt_rectangle_filled(SCREEN_WIDTH - 210, SCREEN_WIDTH - 10, SCREEN_HEIGHT - 40, SCREEN_HEIGHT - 20, arcade.color.GRAY)
        hp_width = 200 * (self.player.health / self.player.max_health)
        arcade.draw_lrbt_rectangle_filled(SCREEN_WIDTH - 210, SCREEN_WIDTH - 210 + hp_width, SCREEN_HEIGHT - 40, SCREEN_HEIGHT - 20, arcade.color.RED)

    def spawn_coins(self):
        self.coins = arcade.SpriteList() 
        self.coins.append(self.coin)
        self.coins.append(self.coin_2)
        self.coins.append(self.coin_3)
        self.coins.append(self.coin_4)

    def on_update(self, delta_time):
        self.player_list.update(delta_time, self.keys_pressed)
        self.coins.update(delta_time)
        self.physics_engine.update()
        self.player.is_on_ground = self.physics_engine.can_jump()
        self.score_label.text = f'Score: {self.player.score}'
        coins_hit = arcade.check_for_collision_with_list(self.player, self.coins)
        for coin in coins_hit:
            self.player.score += coin.value
            coin.remove_from_sprite_lists()
        