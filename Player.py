import arcade


class Player(arcade.Sprite):
    def __init__(self, path,  x, y, width, height, inventory):
        super(Player, self).__init__(path)
        self.screen_w = width
        self.screen_h = height
        self.center_x = x
        self.center_y = y

        # movement
        self.speed = 8
        self.movement_distance = 0
        self.movement_direction = None
        self.look_dir = None
        self.p_class = "k"

        self.inventory = inventory

        # sprites
        self.weapon = None
        self.weapon_list = arcade.SpriteList()

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
        elif key == arcade.key.D:
            self.movement_direction = "right"
            self.movement_distance = dist
            self.look_dir = "right"
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
