from menu_view import MenuView
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_TITLE
from cursor import set_default_cursor
import arcade


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    set_default_cursor(window)
    window.show_view(MenuView())
    arcade.run()


if __name__ == "__main__":
    main()