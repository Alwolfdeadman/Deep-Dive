import arcade
import arcade.gui
import Player
import Enemy
from random import randint
import time

SCREEN_W = 1488  # 1120
SCREEN_H = 848  # 208

""""
-dobavi komentari
- character sprite za dvigenie v vsichki posoki
- inventory
- shops
- lv up
- TESTSSSS
"""


class Game(arcade.View):
    def __init__(self):
        super().__init__()  # call the parent class init to create the window
        # player things
        self.player = None
        self.p_sprite = "assets/TMP/0x72_16x16DungeonTileset.v5/items/npc_dwarf.png"

        # physics and map
        self.room_number = 0
        self.tile_map = None
        self.room_name = None
        self.num_enemies = 0
        self.rooms_passed = 0
        self.dungeon_size = 3
        self.walls = None
        self.scene = None
        self.physics_engine = None
        arcade.set_background_color(arcade.color.BLACK)

        # other useful stuff
        self.start_time = 0
        self.last_button_press = 0
        self.enemies = arcade.SpriteList()

        # text box
        self.text_box = arcade.load_texture("assets/UI/text_box.png")
        self.setup()

    def setup(self):
        self.enemies = arcade.SpriteList()
        r_stats = self.find_cords(self.room_number)
        self.player = Player.Player(self.p_sprite, r_stats[0], r_stats[1], SCREEN_W, SCREEN_H)

        # map/room preping and pyisics
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
            self.walls = (self.scene.get_sprite_list("walls"), self.scene.get_sprite_list("pit1"))
            self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.walls)
        elif self.room_number == 6:
            self.walls = (self.scene.get_sprite_list("walls"), self.scene.get_sprite_list("floor2"))
            self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.walls)
        else:
            self.walls = self.scene.get_sprite_list("walls")
            self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.walls)

        # enemy placement
        for i in range(0, r_stats[4]):
            g_list = self.scene.get_sprite_list("floor")
            while True:
                x = randint(1, 93)
                y = randint(1, 53)
                if arcade.get_sprites_at_point((x*16, y*16), g_list):
                    break
            if self.room_number != 11:
                num = randint(1, 35)
                path = f"assets/melee_monsters/monsters_1/monster{num}.png"
                self.enemies.append(Enemy.Enemy(num, path, self.room_number, x * 16, y * 16, self.player, self.walls))
            else:
                num = randint(1, 3)
                path = f"assets/melee_monsters/bosses/boss{num}.png"
                self.enemies.append(Enemy.Enemy(num, path, self.room_number, 794, 344, self.player, self.walls))
            self.enemies[i].setup_pysics()

    def on_draw(self):
        arcade.start_render()
        self.scene.draw()
        self.player.draw()
        self.player.inventory.draw()
        self.player.inventory.on_draw()
        self.player.weapon_list.draw()
        self.text_box.draw_scaled(560, 744)

        # so that the enemies vanish after death
        for enemy in self.enemies:
            if enemy.health > 1:
                enemy.draw()
            else:
                self.enemies.remove(enemy)

        # used so that the sword stays on screen for a bit
        current_time = time.time()
        if current_time - self.start_time >= 0.6:
            for sword in self.player.weapon_list:
                self.player.weapon_list.remove(sword)
                self.start_time = current_time

    def update(self, delta_time):
        r_stats = self.find_cords(self.room_number)
        self.player.update()
        self.physics_engine.update()

        # check for collision between enemies and enemies and enemies and player
        for enemy in self.enemies:
            enemy.update()
            if arcade.check_for_collision(self.player, enemy):
                self.player.HP -= 20 - self.player.DEF
                tmp = randint(0, 4)
                if tmp == 0:
                    enemy.center_y += 16
                elif tmp == 1:
                    enemy.center_y += -16
                elif tmp == 2:
                    enemy.center_x += 16
                else:
                    enemy.center_x += -16
                if self.player.HP < 1:
                    game_over = GameOver()
                    self.window.show_view(game_over)
                    return
            elif arcade.check_for_collision_with_list(enemy, self.enemies):
                tmp = randint(0, 4)
                if tmp == 0:
                    enemy.center_y += 8
                elif tmp == 1:
                    enemy.center_y += -2
                elif tmp == 2:
                    enemy.center_x += 8
                else:
                    enemy.center_x += -2

        # movement between rooms
        self.num_enemies = len(self.enemies)
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
        self.player.on_key_press(key, modifiers)
        # if key == arcade.key.J:
        #     self.player.attack()

        current_time = time.time()
        if current_time - self.last_button_press >= 0.5:
            if key == arcade.key.J:
                self.last_button_press = current_time
                self.player.attack()

    def on_key_release(self, key, modifiers):
        self.player.on_key_release(key, modifiers)

    def find_cords(self, room_numb):
        tmp = []
        match room_numb:
            case 0:
                tmp.extend([584, 264, 664, 442, 0])
            case 1:
                tmp.extend([568, 76, 567, 614, 11])
            case 2:
                tmp.extend([536, 474, 520, 494, 0])
            case 3:
                tmp.extend([344, 234, 712, 440, 7])
            case 4:
                tmp.extend([568, 442, 360, 264, 5])
            case 5:
                tmp.extend([376, 344, 744, 360, 5])
            case 6:
                tmp.extend([56, 316, 1000, 296, 11])
            case 7:
                tmp.extend([568, 58, 200, 616, 13])
            case 8:
                tmp.extend([568, 154, 554, 584, 10])
            case 9:
                tmp.extend([184, 42, 184, 568, 8])
            case 10:
                tmp.extend([232, 474, 426, 184, 8])
            case 11:
                tmp.extend([184, 346, 872, 344, 1])
            case 12:
                tmp.extend([568, 394, 552, 346, 0])
        return tmp


class GameOver(arcade.View):
    def __init__(self):
        super(GameOver, self).__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.BLACK)
        self.v_box = arcade.gui.UIBoxLayout()

        start_button = arcade.gui.UIFlatButton(text="Restart", width=200)
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
        game_view = Game()
        self.window.show_view(game_view)

    def on_click_quit(self, event):
        arcade.exit()

    def on_draw(self):
        """Draw the game overview"""
        self.clear()
        arcade.draw_text(
            "Game Over",
            SCREEN_W / 2,
            SCREEN_H / 2 + 150,
            arcade.color.BLACK,
            font_size=30,
            anchor_x="center",
        )
        self.manager.draw()

