import arcade
import arcade.gui
import Game

SCREEN_W = 1488
SCREEN_H = 848


class MainMenu(arcade.View):

    def __init__(self):
        super(MainMenu, self).__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.AMETHYST)
        self.v_box = arcade.gui.UIBoxLayout()

        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))
        start_button.on_click = self.on_click_start

        quit_button = arcade.gui.UIFlatButton(text="Quit", width=200)
        self.v_box.add(quit_button)
        quit_button.on_click = self.on_click_quit

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_click_start(self, event):
        game_view = Game.Game()
        self.window.show_view(game_view)

    def on_click_quit(self, event):
        arcade.exit()

    def on_draw(self):
        """Draw the game overview"""
        self.clear()
        arcade.draw_text(
            "Deep Dive",
            SCREEN_W / 2,
            SCREEN_H / 2 + 150,
            arcade.color.BLACK,
            font_size=30,
            anchor_x="center",
        )
        self.manager.draw()


def main():
    window = arcade.Window(SCREEN_W, SCREEN_H, "DeepDive")
    menu_view = MainMenu()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
