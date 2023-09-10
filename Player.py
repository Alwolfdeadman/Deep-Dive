import arcade
import Inventory


class Player(arcade.Sprite):
    def __init__(self, path,  x, y, width, height):
        super(Player, self).__init__()
        self.screen_w = width
        self.screen_h = height
        self.center_x = x
        self.center_y = y

        self.inventory = Inventory.Inventory("assets/UI/inventory.png")
        self.inventory.hp = self.inventory.max_HP

        # movement
        self.speed = 8
        self.movement_distance = 0
        self.movement_direction = None
        self.look_dir = None
        self.p_class = "k"

        # sprites
        self.weapon = None
        self.weapon_list = arcade.SpriteList()
        self.player_sprites = [arcade.load_texture(path), arcade.load_texture(path, flipped_horizontally=True)]
        self.texture = self.player_sprites[1]


    def update(self):
        if self.movement_distance > 0:
            if self.movement_direction == "up":
                self.center_y += self.speed
            elif self.movement_direction == "down":
                self.center_y -= self.speed
            elif self.movement_direction == "left":
                self.center_x -= self.speed
            elif self.movement_direction == "right":
                self.center_x += self.speed
            self.movement_distance -= self.speed
        else:
            self.movement_direction = None

        if self.left < 0:
            self.left = 0
        elif self.right > self.screen_w - 1:
            self.right = self.screen_w - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > self.screen_h - 1:
            self.top = self.screen_h - 1

    def on_key_press(self, key, modifiers):
        dist = 16
        if key == arcade.key.W:
            self.movement_direction = "up"
            self.movement_distance = dist
            self.look_dir = "up"
        elif key == arcade.key.S:
            self.movement_direction = "down"
            self.movement_distance = dist
            self.look_dir = "down"
        elif key == arcade.key.A:
            self.movement_direction = "left"
            self.movement_distance = dist
            self.look_dir = "left"
            self.texture = self.player_sprites[1]
        elif key == arcade.key.D:
            self.movement_direction = "right"
            self.movement_distance = dist
            self.look_dir = "right"
            self.texture = self.player_sprites[0]
        elif key == arcade.key.K:
            self.inventory.use_pot()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S:
            self.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.change_x = 0

    def attack(self):
        if self.look_dir == "up":
            self.weapon = arcade.Sprite("assets/character_classes_and_animations/weapons/swords/sword_up.png")
            self.weapon.center_x = self.center_x
            self.weapon.center_y = self.center_y + 16
        elif self.look_dir == "down":
            self.weapon = arcade.Sprite("assets/character_classes_and_animations/weapons/swords/sword_down.png")
            self.weapon.center_x = self.center_x
            self.weapon.center_y = self.center_y - 17
        elif self.look_dir == "left":
            self.weapon = arcade.Sprite("assets/character_classes_and_animations/weapons/swords/sword_left.png")
            self.weapon.center_x = self.center_x - 18
            self.weapon.center_y = self.center_y
        elif self.look_dir == "right":
            self.weapon = arcade.Sprite("assets/character_classes_and_animations/weapons/swords/sword_right.png")
            self.weapon.center_x = self.center_x + 16
            self.weapon.center_y = self.center_y
        else:
            self.weapon = arcade.Sprite("assets/character_classes_and_animations/weapons/swords/sword_right.png")
            self.weapon.center_x = self.center_x + 16
            self.weapon.center_y = self.center_y
        self.weapon_list.append(self.weapon)

    def add_gold(self, gold):
        self.inventory.add_gold(gold)

    def add_pot(self):
        self.inventory.add_pot()

    def upgrade_sword(self):
        self.inventory.uprgrade_sword()

    def upgrade_helm(self):
        self.inventory.uprgrade_helm()

    def upgrade_chestplate(self):
        self.inventory.uprgrade_chestplate()

    def enhance_vit(self):
        self.inventory.enhance_vit()

    def enhance_str(self):
        self.inventory.enhance_str()

    def enhance_end(self):
        self.inventory.enhance_end()
