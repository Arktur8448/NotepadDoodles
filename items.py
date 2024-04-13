import arcade


class Item(arcade.Sprite):
    def __init__(self, sprite_path, name, description="", item_rarity="Common", price_buy=1, price_sell=1):
        super().__init__(filename=sprite_path, scale=1)
        self.name = name
        self.description = description
        self.item_rarity = item_rarity
        self.price_buy = price_buy
        self.price_sell = price_sell


class Weapon(Item):
    def __init__(self, sprite_path, name, description="", item_rarity="Common", price_buy=1, price_sell=1, damage=1, speed=1, attack_range=1, slash_scale=1):
        super().__init__(sprite_path, name, description, item_rarity, price_buy, price_sell)
        self.damage = damage
        self.speed = speed
        self._cooldown_counter = 0
        self.attack_range = int(attack_range * 300)
        self.canAttack = True
        self.slash_scale = slash_scale

    def cooldown(self):
        self._cooldown_counter -= 1/60
        if self._cooldown_counter <= 0:
            self.canAttack = True

    def start_cooldown(self):
        self._cooldown_counter = self.speed
        self.canAttack = False
