import arcade
import Player
from random import randint
import time

SCREEN_W = 1480
SCREEN_H = 840

""""
-dobavi komentari
- character sprite za dvigenie v vsichki posoki
- ataka na geroq
- enemi class
"""


class Game(arcade.Window):

    def __init__(self, w, h, t):
        super().__init__(w, h, t)  # call the parent class init to create the window

        self.p_list = None
        self.player = None
        self.p_sprite = "assets/TMP/0x72_16x16DungeonTileset.v5/items/npc_dwarf.png"

        self.room_number = 1
        self.tile_map = None
        self.room_name = None
        self.num_enemies = 0
        self.rooms_passed = 0
        self.dungeon_size = 1

        self.scene = None
        self.physics_engine = None
        
        arcade.set_background_color(arcade.color.DARK_RED)
        self.start_time = 0
        self.last_button_press = 0

    def setup(self):
        r_stats = self.find_cords(self.room_number)
        self.p_list = arcade.SpriteList()
        self.player = Player.Player(self.p_sprite, r_stats[0], r_stats[1], SCREEN_W, SCREEN_H)
        self.p_list.append(self.player)

        self.room_name = f"assets/maps/room{self.room_number}.tmx"
        layer_options = {
            "walls": {
                "use_spatial_hash": True,
            }
        }
        self.tile_map = arcade.load_tilemap(self.room_name, 1, layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)
        if self.room_number == 2:
            self.physics_engine = arcade.PhysicsEngineSimple(self.player, (self.scene.get_sprite_list("walls"),
                                                                           self.scene.get_sprite_list("pit1")))
        elif self.room_number == 6:
            self.physics_engine = arcade.PhysicsEngineSimple(self.player, (self.scene.get_sprite_list("walls"),
                                                                           self.scene.get_sprite_list("floor2")))
        else:
            self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.scene.get_sprite_list("walls"))

    def on_draw(self):
        arcade.start_render()
        self.scene.draw()
        self.player.draw()
        self.player.weapon_list.draw()

        current_time = time.time()
        if current_time - self.start_time >= 0.7:
            for sword in self.player.weapon_list:
                self.player.weapon_list.remove(sword)
                self.start_time = current_time

    def update(self, delta_time):
        r_stats = self.find_cords(self.room_number)
        self.player.update()
        self.physics_engine.update()

        if (
                r_stats[2] <= self.player.center_x <= (r_stats[2] + 16)
                and r_stats[3] <= self.player.center_y <= r_stats[3] + 16
                and self.num_enemies == 0 and self.rooms_passed < self.dungeon_size - 1
                or (
                    r_stats[2] <= self.player.center_x <= (r_stats[2] + 48)
                    and r_stats[3] <= self.player.center_y <= r_stats[3] + 16
                    and self.num_enemies == 0 and self.rooms_passed < self.dungeon_size - 1
                    and self.room_number == 2
                   )
           ):
            self.room_number = randint(1, 10)
            self.rooms_passed += 1
            self.setup()
        elif (
                    r_stats[2] <= self.player.center_x <= (r_stats[2] + 16)
                and r_stats[3] <= self.player.center_y <= r_stats[3] + 16
                and self.num_enemies == 0 and self.rooms_passed == self.dungeon_size - 1
             ):
            self.room_number = 11
            self.rooms_passed += 1
            self.setup()
        elif (
                    r_stats[2] <= self.player.center_x <= (r_stats[2] + 16)
                and r_stats[3]-16 <= self.player.center_y <= r_stats[3] + 16
                and self.num_enemies == 0 and self.room_number == 11
             ):
            self.room_number = 12
            self.rooms_passed += 1
            self.setup()
        elif (
                    r_stats[2] <= self.player.center_x <= (r_stats[2] + 16)
                and r_stats[3] <= self.player.center_y <= r_stats[3] + 16
                and self.num_enemies == 0 and self.room_number == 12
             ):
            self.room_number = 0
            self.rooms_passed = 0
            self.setup()

    def on_key_press(self, key, modifiers):
        enemy = None
        self.player.on_key_press(key, modifiers)
        # if key == arcade.key.J:
        #     self.player.attack()

        current_time = time.time()
        if current_time - self.last_button_press >= 0.5:
            if key == arcade.key.J:
                self.last_button_press = current_time
                self.player.attack(enemy)

    def on_key_release(self, key, modifiers):
        self.player.on_key_release(key, modifiers)

    def find_cords(self, room_numb):
        tmp = []
        match room_numb:
            case 0:
                tmp.extend([584, 264, 664, 442])
            case 1:
                tmp.extend([568, 76, 567, 614])
            case 2:
                tmp.extend([536, 474, 520, 494])
            case 3:
                tmp.extend([344, 234, 712, 440])
            case 4:
                tmp.extend([568, 442, 360, 264])
            case 5:
                tmp.extend([376, 344, 744, 360])
            case 6:
                tmp.extend([56, 316, 1000, 296])
            case 7:
                tmp.extend([568, 58, 200, 616])
            case 8:
                tmp.extend([568, 154, 554, 584])
            case 9:
                tmp.extend([184, 42, 184, 568])
            case 10:
                tmp.extend([232, 474, 426, 184])
            case 11:
                tmp.extend([184, 346, 872, 344])
            case 12:
                tmp.extend([568, 394, 552, 346])
        return tmp


def main():
    window = Game(SCREEN_W, SCREEN_H, "asa")
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
