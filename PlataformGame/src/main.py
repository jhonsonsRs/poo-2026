from game_view import GameView
import arcade

def main():
    window = arcade.Window(800, 600, "Plataformer")
    window.show_view(GameView())
    arcade.run()

if __name__ == "__main__":
    main()