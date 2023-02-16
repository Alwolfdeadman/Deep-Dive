import arcade
import Player
from random import randint


class Enemy(arcade.Sprite):

    def __init__(self, num, path, room_count, x, y, player):
        super().__init__(path)
        self.player = player
        self.center_x = x
        self.center_y = y
        self.health = randint(7, 10)*room_count

        self.num_of_monster = num

        self.damaging_textures = arcade.SpriteList()

        self.mon_lst = arcade.SpriteList()
        for i in range(1, 36):
            tmp = arcade.Sprite(f"assets/melee_monsters/monsters_1/monster{i}.png")
            self.mon_lst.append(tmp)
        self.mon_lst.append(self.player)

    def update(self):
        self.damaging_textures.clear()
        self.damaging_textures.extend(self.player.weapon_list)

        if self.player.center_x == self.center_x:
            self.center_x += 0
        elif self.player.center_x < self.center_x:
            self.center_x += -0.5
        elif self.player.center_x > self.center_x:
            self.center_x += 0.5
        if self.player.center_y == self.center_y:
            self.center_y += 0
        elif self.player.center_y < self.center_y:
            self.center_y += -0.5
        elif self.player.center_y > self.center_y:
            self.center_y += 0.5

#they still aline and move as one
        col_lst = arcade.check_for_collision_with_lists(self, [self.damaging_textures, self.mon_lst])
        for sprite in self.mon_lst:
            if arcade.check_for_collision(self, sprite):
                tmp = randint(0, 4)
                if isinstance(sprite, Player.Player):
                    if tmp == 0:
                        self.center_y += 8
                    elif tmp == 1:
                        self.center_y += -2
                    elif tmp == 2:
                        self.center_x += 8
                    else:
                        self.center_x += -2
                else:
                    if tmp == 0:
                        self.center_y += 16
                    elif tmp == 1:
                        self.center_y += -16
                    elif tmp == 2:
                        self.center_x += 16
                    else:
                        self.center_x += -16

        for dam in self.damaging_textures:
            if arcade.check_for_collision(dam, self):
                print(self.health)
                self.health -= self.player.attack_power
                break
