from game_view import GameView
from constants import SCREEN_HEIGHT, SCREEN_WIDTH   
import arcade

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Plataformer")
    window.show_view(GameView())
    arcade.run()

if __name__ == "__main__":
    main()