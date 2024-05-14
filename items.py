import random

import arcade


class Item(arcade.Sprite):
    def __init__(self, sprite_path, name, price_buy=0):
        super().__init__(filename=sprite_path, scale=1)
        self.name = name
        self.price_buy = price_buy


class Weapon(Item):
    def __init__(self, sprite_path, name, price_buy=0, damage=1,
                 speed=1, attack_range=1, slash_scale=1):
        super().__init__(sprite_path, name, price_buy)
        self.damage = damage
        self.speed = speed
        self._cooldown_counter = 0
        self.attack_range = int(attack_range * 200)
        self.canAttack = True
        self.slash_scale = slash_scale

    def cooldown(self):
        self._cooldown_counter -= 1 / 60
        if self._cooldown_counter <= 0:
            self.canAttack = True

    def start_cooldown(self):
        self._cooldown_counter = self.speed
        self.canAttack = False


class RangedWeapon(Item):
    def __init__(self, sprite_path, bullet_path, name, price_buy=0,
                 damage=1, speed=1, attack_range=1, bullet_speed=1):
        super().__init__(sprite_path, name, price_buy)
        self.bullet_path = bullet_path
        self.damage = damage
        self.speed = speed
        self.bullet_speed = bullet_speed * 300
        self._cooldown_counter = 0
        self.attack_range = int(attack_range * 300)
        self.canAttack = True

    def cooldown(self):
        self._cooldown_counter -= 1 / 60
        if self._cooldown_counter <= 0:
            self.canAttack = True

    def start_cooldown(self):
        self._cooldown_counter = self.speed
        self.canAttack = False


class Wand(Item):
    def __init__(self, sprite_path, bullet_path, name,  price_buy=0,
                 damage=1, speed=1, attack_range=1, bullet_speed=1):
        super().__init__(sprite_path, name, price_buy)
        self.bullet_path = bullet_path
        self.damage = damage
        self.speed = speed
        self.bullet_speed = bullet_speed * 300
        self._cooldown_counter = 0
        self.attack_range = int(attack_range * 300)
        self.canAttack = True

    def cooldown(self):
        self._cooldown_counter -= 1 / 60
        if self._cooldown_counter <= 0:
            self.canAttack = True

    def start_cooldown(self):
        self._cooldown_counter = self.speed
        self.canAttack = False


class Ring(Item):
    def __init__(self, sprite_path, name, price_buy=0, statistic_to_modify=None, text_to_display=None, percentage_range=(10, 30)):
        super().__init__(sprite_path, name, price_buy)
        self.statistic_to_modify = statistic_to_modify
        self.percentage_range = percentage_range
        self.percentage = random.randint(self.percentage_range[0], percentage_range[1])
        self.start_price_buy = price_buy
        self.price_buy = self.start_price_buy
        if not text_to_display:
            self.text_to_display = self.statistic_to_modify
        else:
            self.text_to_display = text_to_display

        self.added_value = 0

    def apply(self, player):
        current_value = getattr(player, self.statistic_to_modify)
        self.added_value = current_value * self.percentage/100
        setattr(player, self.statistic_to_modify, current_value + current_value * self.percentage/100)

    def deapply(self, player):
        current_value = getattr(player, self.statistic_to_modify)
        setattr(player, self.statistic_to_modify, current_value - self.added_value)

    def regenerate(self):
        self.percentage = random.randint(self.percentage_range[0], self.percentage_range[1])
        self.price_buy = self.start_price_buy + abs(int(self.start_price_buy * (self.percentage / 100 * 2)))


class Potion(Item):
    def __init__(self, sprite_path, name, price_buy=0, amount=0):
        super().__init__(sprite_path, name, price_buy)
        self.amount = amount
