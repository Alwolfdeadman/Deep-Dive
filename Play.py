import arcade
import Game

SCREEN_W = 1488
SCREEN_H = 848


class MainMenu(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.AMETHYST)

    def on_draw(self):
        """Draw the menu"""
        self.clear()
        arcade.draw_text(
            "Play",
            SCREEN_W / 2,
            SCREEN_H / 2 + 50,
            arcade.color.BLACK,
            font_size=30,
            anchor_x="center",
        )
        arcade.draw_text(
            "Exit",
            SCREEN_W / 2,
            SCREEN_H / 2 - 50,
            arcade.color.BLACK,
            font_size=30,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the 'game' view."""
        game_view = Game.Game()
        self.window.show_view(game_view)


def main():
    window = arcade.Window(SCREEN_W, SCREEN_H, "DeepDive")
    menu_view = MainMenu()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
