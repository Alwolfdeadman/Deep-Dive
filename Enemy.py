import arcade
from random import randint


class Enemy(arcade.Sprite):

    def __init__(self, num, room_count, x, y):
        super().__init__(f"assets/melee_monsters/monsters_1/monster{num}.png")
        self.center_x = x
        self.center_y = y
        self.health = randint(7, 10)*room_count

        self.num_of_monster = num

        self.damaging_textures = []
        self.damaging_textures.append(
            arcade.load_texture("assets/character_classes_and_animations/weapons/swords/sword_up.png"))
        self.damaging_textures.append(
            arcade.load_texture("assets/character_classes_and_animations/weapons/swords/sword_down.png"))
        self.damaging_textures.append(
            arcade.load_texture("assets/character_classes_and_animations/weapons/swords/sword_left.png"))
        self.damaging_textures.append(
            arcade.load_texture("assets/character_classes_and_animations/weapons/swords/sword_right.png"))
