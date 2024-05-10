import arcade


class Item(arcade.Sprite):
    def __init__(self, sprite_path, name, price_buy=1):
        super().__init__(filename=sprite_path, scale=1)
        self.name = name
        self.price_buy = price_buy


class Weapon(Item):
    def __init__(self, sprite_path, name, price_buy=1, damage=1,
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
    def __init__(self, sprite_path, bullet_path, name, price_buy=1,
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
    def __init__(self, sprite_path, bullet_path, name,  price_buy=1,
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


