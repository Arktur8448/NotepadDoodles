class Perks:
    def __init__(self, name, description, hp_increase, mana_increase, strength_increase, defence_increase, agility_increase, special_effects):
        self.name = name
        self.perk_level = 0
        self.description = description
        self.hp_increase = hp_increase * (self.perk_level*0.5)
        self.mana_increase = mana_increase
        self.strength_increase = strength_increase
        self.defence_increase = defence_increase
        self.agility_increase = agility_increase
        self.special_effects = special_effects
