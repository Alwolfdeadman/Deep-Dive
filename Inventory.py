import arcade


class Inventory(arcade.Sprite):
    def __init__(self, path):
        super(Inventory, self).__init__(path)
        self.image = None
        self.center_x = 1304
        self.center_y = 360

        # stats
        self.vit = 0
        self.end = 0
        self.str = 0

        self.hp = 0
        self.dps = 0
        self.deff = 0

        # items
        self.pots = 0
        self.gold = 100
        self.helm = None
        self.chestplate = None
        self.sword = None
