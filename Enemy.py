import arcade
import Player
from random import randint


class Enemy(arcade.Sprite):

    def __init__(self, num, path, room_count, x, y, player, walls):
        super().__init__(path)
        self.player = player
        self.walls = walls
        self.center_x = x
        self.center_y = y
        self.health = randint(7, 10)*room_count

        self.num_of_monster = num

        self.physics_engine = None
        self.damaging_textures = arcade.SpriteList()
        self.mon_lst = arcade.SpriteList()
        for i in range(1, 36):
            tmp = arcade.Sprite(f"assets/melee_monsters/monsters_1/monster{i}.png")
            self.mon_lst.append(tmp)
        self.mon_lst.append(self.player)

    def setup_pysics(self):
        self.physics_engine = arcade.PhysicsEngineSimple(self, self.walls)

    def update(self):
        self.damaging_textures.clear()
        self.damaging_textures.extend(self.player.weapon_list)
        self.physics_engine.update()

        # to follow the player
        if self.player.center_x == self.center_x:
            self.center_x += 0
        elif self.player.center_x < self.center_x:
            self.center_x += -0.3
        elif self.player.center_x > self.center_x:
            self.center_x += 0.3
        if self.player.center_y == self.center_y:
            self.center_y += 0
        elif self.player.center_y < self.center_y:
            self.center_y += -0.3
        elif self.player.center_y > self.center_y:
            self.center_y += 0.3

        # to take damage from attacks
        for dam in self.damaging_textures:
            if arcade.check_for_collision(dam, self):
                self.health -= self.player.attack_power
                break
