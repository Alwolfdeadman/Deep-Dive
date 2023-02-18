import arcade
import arcade.gui
import Player
import Inventory
import Enemy
from random import randint
import time

SCREEN_W = 1488  # 1120
SCREEN_H = 848  # 208

""""
- chests
- TESTSSSS
"""


class Game(arcade.View):
    def __init__(self):
        super().__init__()  # call the parent class init to create the window
        # player things
        self.player = None
        self.p_sprite = "assets/character_classes_and_animations/npc_dwarf.png"
        self.p_invent = Inventory.Inventory("assets/UI/inventory.png")
        arcade.set_background_color(arcade.color.BLACK)

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

        # other useful stuff
        self.start_time = 0
        self.last_button_press = 0
        self.enemies = arcade.SpriteList()

        # text box
        self.text_box = arcade.load_texture("assets/UI/text_box.png")
        self.setup()

        # shop
        self.shop = arcade.Sprite("assets/npcs/npc_sage.png", center_x=440, center_y=200,)
        self.shop_active = False
        self.manager1 = arcade.gui.UIManager()
        buy_pot_button = arcade.gui.UIFlatButton(x=200, y=750, text="Buy Pots", width=100, height=30, style={
            "border_width": 0,
            "border_radius": 10,
            "bg_color": arcade.color.CHARCOAL,
        })
        buy_pot_button.on_click = self.on_click_add_pots
        self.manager1.add(buy_pot_button)

        #blacksmith
        self.b_smith = arcade.Sprite("assets/npcs/npc_dwarf_2.png", center_x=440, center_y=296)
        self.b_smith_active = False
        self.manager2 = arcade.gui.UIManager()
        upgrade_sword_button = arcade.gui.UIFlatButton(x=200, y=750, text="Upgrade Sword", width=200, height=30, style={
            "border_width": 0,
            "border_radius": 10,
            "bg_color": arcade.color.CHARCOAL,
        })
        upgrade_chestplate_button = arcade.gui.UIFlatButton(x=430, y=750, text="Upgrade Chestplate", width=240, height=30, style={
            "border_width": 0,
            "border_radius": 10,
            "bg_color": arcade.color.CHARCOAL,
        })
        upgrade_helm_button = arcade.gui.UIFlatButton(x=700, y=750, text="Upgrade Helm", width=200, height=30, style={
            "border_width": 0,
            "border_radius": 10,
            "bg_color": arcade.color.CHARCOAL,
        })
        upgrade_sword_button.on_click = self.on_click_upgrade_sword
        upgrade_chestplate_button.on_click = self.on_click_upgrade_chestplate
        upgrade_helm_button.on_click = self.on_click_upgrade_helm
        self.manager2.add(upgrade_sword_button)
        self.manager2.add(upgrade_chestplate_button)
        self.manager2.add(upgrade_helm_button)

        # LV mage
        self.lv_mage = arcade.Sprite("assets/npcs/npc_wizzard_1.png", center_x=678, center_y=216)
        self.lv_mage_active = False
        self.manager3 = arcade.gui.UIManager()
        enhance_vit_button = arcade.gui.UIFlatButton(x=200, y=750, text="Enhance VIT", width=200, height=30, style={
            "border_width": 0,
            "border_radius": 10,
            "bg_color": arcade.color.CHARCOAL,
        })
        enhance_str_button = arcade.gui.UIFlatButton(x=430, y=750, text="Enhance STR", width=240, height=30, style={
            "border_width": 0,
            "border_radius": 10,
            "bg_color": arcade.color.CHARCOAL,
        })
        enhance_end_button = arcade.gui.UIFlatButton(x=700, y=750, text="Enhance END", width=200, height=30, style={
            "border_width": 0,
            "border_radius": 10,
            "bg_color": arcade.color.CHARCOAL,
        })
        enhance_vit_button.on_click = self.on_click_enhance_vit
        enhance_str_button.on_click = self.on_click_enhance_str
        enhance_end_button.on_click = self.on_click_enhance_end
        self.manager3.add(enhance_vit_button)
        self.manager3.add(enhance_str_button)
        self.manager3.add(enhance_end_button)

    def setup(self):
        self.enemies = arcade.SpriteList()
        r_stats = self.find_cords(self.room_number)
        self.player = Player.Player(self.p_sprite, r_stats[0], r_stats[1], SCREEN_W, SCREEN_H, self.p_invent)

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
        if self.room_number == 0:
            self.shop.draw()
            self.b_smith.draw()
            self.lv_mage.draw()
            if self.shop_active:
                arcade.draw_text(
                    "Wanna buy some goods, Ya kno'i got the goood stuff.",
                    400,
                    800,
                    arcade.color.BLACK,
                    font_size=16,
                    anchor_x="center",
                )
                self.manager1.draw()
            elif self.b_smith_active:
                arcade.draw_text(
                    "Ya in need of smithing.",
                    400,
                    800,
                    arcade.color.BLACK,
                    font_size=16,
                    anchor_x="center",
                )
                self.manager2.draw()
            elif self.lv_mage_active:
                arcade.draw_text(
                    "What enhancements would you wish for today.",
                    400,
                    800,
                    arcade.color.BLACK,
                    font_size=16,
                    anchor_x="center",
                )
                self.manager3.draw()

        # so that the enemies vanish after death
        for enemy in self.enemies:
            if enemy.health > 1:
                enemy.draw()
            else:
                if self.room_number == 11:
                    self.p_invent.gold += 30*self.room_number
                else:
                    self.p_invent.gold += 10*self.room_number
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
                if self.room_number == 11:
                    self.player.inventory.hp -= (40 - self.player.inventory.deff)
                else:
                    self.player.inventory.hp -= (20 - self.player.inventory.deff)
                tmp = randint(0, 4)
                if tmp == 0:
                    enemy.center_y += 16
                elif tmp == 1:
                    enemy.center_y += -16
                elif tmp == 2:
                    enemy.center_x += 16
                else:
                    enemy.center_x += -16
                if self.player.inventory.hp < 1:
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

        current_time = time.time()
        if current_time - self.last_button_press >= 0.5:
            if key == arcade.key.J:
                self.last_button_press = current_time
                self.player.attack()
        spr_lst = arcade.SpriteList()
        spr_lst.append(self.shop)
        spr_lst.append(self.b_smith)
        spr_lst.append(self.lv_mage)
        if key == arcade.key.L and self.shop in arcade.get_sprites_at_point((self.player.center_x - 16, self.player.center_y), spr_lst):
            self.shop_active = True
            self.b_smith_active = False
            self.lv_mage_active = False
            self.manager1.enable()
        elif key == arcade.key.L and self.b_smith in arcade.get_sprites_at_point((self.player.center_x - 16, self.player.center_y), spr_lst):
            self.b_smith_active = True
            self.shop_active = False
            self.lv_mage_active = False
            self.manager2.enable()
        elif key == arcade.key.L and self.lv_mage in arcade.get_sprites_at_point((self.player.center_x + 16, self.player.center_y), spr_lst):
            self.lv_mage_active = True
            self.b_smith_active = False
            self.shop_active = False
            self.manager3.enable()
        else:
            self.lv_mage_active = False
            self.b_smith_active = False
            self.shop_active = False

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

    def on_click_add_pots(self, event):
        if self.p_invent.gold >= 35:
            self.p_invent.pots += 1
            self.p_invent.gold -= 35

    def on_click_upgrade_sword(self, event):
        mod = self.p_invent.sword[2]
        if self.p_invent.gold >= 100*mod:
            self.p_invent.gold -= 100*mod
            self.p_invent.sword = [5*(mod+1), f"assets/items/swords/sword_{mod + 1}.png", mod + 1]
            self.p_invent.dps = 10 + self.p_invent.str * 5 + self.p_invent.sword[0]

    def on_click_upgrade_chestplate(self, event):
        mod = self.p_invent.chestplate[2]
        if self.p_invent.gold >= 150 * mod:
            self.p_invent.gold -= 150 * mod
            self.p_invent.chestplate = [10 * (mod + 1), f"assets/items/chestplates/chestplate_{mod + 1}.png", mod + 1]
            self.p_invent.deff = 0 + self.p_invent.end * 2 + (self.p_invent.chestplate[0] + self.p_invent.helm[0]) / 2

    def on_click_upgrade_helm(self, event):
        mod = self.p_invent.helm[2]
        if self.p_invent.gold >= 75 * mod:
            self.p_invent.gold -= 75 * mod
            self.p_invent.helm = [10 * (mod + 1), f"assets/items/helmet/helm_{mod + 1}.png", mod + 1]
            self.p_invent.deff = 0 + self.p_invent.end * 2 + (self.p_invent.chestplate[0] + self.p_invent.helm[0]) / 2

    def on_click_enhance_vit(self, event):
        mod = self.p_invent.vit
        if self.p_invent.gold >= 50*mod:
            self.p_invent.gold -= 50*mod
            self.p_invent.vit += 1
            self.p_invent.hp = 90 + self.p_invent.vit * 10
            self.p_invent.max_HP = self.p_invent.hp

    def on_click_enhance_str(self, event):
        mod = self.p_invent.str
        if self.p_invent.gold >= 50*mod:
            self.p_invent.gold -= 50*mod
            self.p_invent.str += 1
            self.p_invent.dps = 10 + self.p_invent.str * 5 + self.p_invent.sword[0]

    def on_click_enhance_end(self, event):
        mod = self.p_invent.end
        if self.p_invent.gold >= 50*mod:
            self.p_invent.gold -= 50*mod
            self.p_invent.end += 1
            self.p_invent.deff = 0 + self.p_invent.end * 2 + (self.p_invent.chestplate[0] + self.p_invent.helm[0]) / 2


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
