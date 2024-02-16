import arcade

class NPC (arcade.Sprite):
    def __init__(self, filename, name, description, pos_x, pos_y, level=1, exp_drop=0, health=1, strength=1, defence=1, agility=1,speed=1, race=None,
                 weapon=None, drop=None, to_sell=None):
        super().__init__(filename=filename, center_x=pos_x, center_y=pos_y, scale=0.5)
        self.name = name
        self.description = description
        self.level = level
        self.exp_drop = exp_drop
        self.health = health
        self.max_health = self.health
        self.strength = strength
        self.defence = defence
        self.agility = agility
        self.speed = speed
        self.race = race
        self.weapon = weapon if weapon else []
        self.drop = drop if drop else []
        self.to_sell = to_sell if to_sell else []
        # jako tablica 2 wymiarowa [[(tutaj dajesz item który zrobisz używając klasy), cena], itd...] np.: (Health_Potion, Health_Potion.price_buy

    def is_alive(self):
        if self.health > 0:
            return True
        else:
            return False

    def show_health(self):
        hp = arcade.Text(
            f"HP: {int(self.health)}/{self.max_health}",
            self.center_x - 60,
            self.center_y + 40,
            arcade.color.RED,
            15,
            font_name="Kenney Blocks",
        )
        return hp



