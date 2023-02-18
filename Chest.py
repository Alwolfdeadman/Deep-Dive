import arcade
from random import randint


class Chest(arcade.Sprite):
    def __init__(self, path, x, y, player, inventory):
        super(Chest, self).__init__(path)
        self.p = player
        self.center_y = y
        self.center_x = x
        self.if_openable = True
        self.invent = inventory

    def update(self):
        if arcade.check_for_collision(self.p, self) and self.if_openable:
            self.if_openable = False
            what_to_add = randint(1, 100)
            if what_to_add in range(28, 100):
                self.invent.gold += randint(50, 100)
            elif what_to_add in range(1, 9):
                self.invent.vit += 1
            elif what_to_add in range(10, 18):
                self.invent.str += 1
            elif what_to_add in range(19, 27):
                self.invent.end += 1

