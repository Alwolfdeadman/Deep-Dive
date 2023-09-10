import arcade


class Inventory(arcade.Sprite):
    def __init__(self, path):
        super(Inventory, self).__init__(path)
        self.image = None
        self.center_x = 1304
        self.center_y = 360

        # items
        self.pots = 2
        self.gold = 100
        self.helm = [10, "assets/items/helmet/helm_1.png", 1]
        self.chestplate = [10, "assets/items/chestplates/chestplate_1.png", 1]
        self.sword = [5, "assets/items/swords/sword_1.png", 1]

        # stats
        self.vit = 1
        self.end = 1
        self.str = 1

        self.max_HP = 90 + self.vit * 10
        self.hp = 90 + self.vit * 10
        self.dps = 10 + self.str * 5 + self.sword[0]
        self.deff = 0 + self.end * 2 + (self.chestplate[0] + self.helm[0]) / 2

    def on_draw(self):
        # show the current level of equipment
        sword = arcade.Sprite(self.sword[1], scale=2)
        sword.center_x = 1220
        sword.center_y = 482
        sword.draw()

        chestplate = arcade.Sprite(self.chestplate[1], scale=1.5)
        chestplate.center_x = 1378
        chestplate.center_y = 474
        chestplate.draw()

        helm = arcade.Sprite(self.helm[1], scale=1.5)
        helm.center_x = 1300
        helm.center_y = 564
        helm.draw()

        arcade.draw_text(
            self.gold,
            1260,
            378,
            arcade.color.BLACK,
            font_size=16,
            anchor_x="center",
        )
        arcade.draw_text(
            self.pots,
            1398,
            378,
            arcade.color.BLACK,
            font_size=16,
            anchor_x="center",
        )
        arcade.draw_text(
            self.vit,
            1250,
            328,
            arcade.color.BLACK,
            font_size=16,
            anchor_x="center",
        )
        arcade.draw_text(
            self.str,
            1250,
            278,
            arcade.color.BLACK,
            font_size=16,
            anchor_x="center",
        )
        arcade.draw_text(
            self.end,
            1250,
            230,
            arcade.color.BLACK,
            font_size=16,
            anchor_x="center",
        )
        arcade.draw_text(
            self.hp,
            1400,
            332,
            arcade.color.BLACK,
            font_size=16,
            anchor_x="center",
        )
        arcade.draw_text(
            self.dps,
            1400,
            282,
            arcade.color.BLACK,
            font_size=16,
            anchor_x="center",
        )
        arcade.draw_text(
            self.deff,
            1410,
            234,
            arcade.color.BLACK,
            font_size=16,
            anchor_x="center",
        )

    def use_pot(self):
        if self.pots > 0:
            self.pots -= 1
            self.hp = (self.hp + 50) if (self.hp + 50) < self.max_HP else self.max_HP

    def add_gold(self, gold):
        self.gold += gold

    def add_pot(self):
        if self.gold >= 35:
            self.pots += 1
            self.gold -= 35

    def uprgrade_helm(self):
        if self.gold >= 75 * self.helm[2]:
            self.gold -= 75 * self.helm[2]
            self.helm = [
                10 * (self.helm[2] + 1), f"assets/items/helmet/helm_{self.helm[2] + 1}.png", self.helm[2] + 1]
            self.deff = 0 + self.end * 2 + (self.chestplate[0] + self.helm[0]) / 2

    def uprgrade_sword(self):
        if self.gold >= 100 * self.sword[2]:
            self.gold -= 100 * self.sword[2]
            self.sword = \
                [5 * (self.sword[2] + 1), f"assets/items/swords/sword_{self.sword[2] + 1}.png", self.sword[2] + 1]
            self.dps = 10 + self.str * 5 + self.sword[0]

    def uprgrade_chestplate(self):
        if self.gold >= 150 * self.chestplate[2]:
            self.gold -= 150 * self.chestplate[2]
            self.chestplate = \
                [10 * (self.chestplate[2] + 1), f"assets/items/chestplates/chestplate_{self.chestplate[2] + 1}.png", self.chestplate[2] + 1]
            self.deff = 0 + self.end * 2 + (self.chestplate[0] + self.helm[0]) / 2

    def enhance_vit(self):
        if self.gold >= 50*self.vit:
            self.gold -= 50*self.vit
            self.vit += 1
            self.hp = 90 + self.vit * 10
            self.max_HP = self.hp

    def enhance_str(self):
        if self.gold >= 50*self.str:
            self.gold -= 50*self.str
            self.str += 1
            self.dps = 10 + self.str * 5 + self.sword[0]

    def enhance_end(self):
        if self.gold >= 50*self.end:
            self.gold -= 50*self.end
            self.end += 1
            self.deff = 0 + self.end * 2 + (self.chestplate[0] + self.helm[0]) / 2

