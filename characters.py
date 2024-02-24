class Character:
    def __init__(self, name="", desc="",
                 base_hp=1, base_hp_regen_rate=1, base_stamina=1, base_stamina_regen_rate=1,
                 base_strength=1, base_defence=1, base_agility=1, base_dodge=1, base_accuracy=1,
                 base_movement_speed=1,
                 base_dash_distance=1, base_dash_cooldown=1, base_dash_duration=1):
        self.name = name
        self.desc = desc
        self.detailed_desc_addition = None

        # Base stats Multiplayer
        self.base_hp = base_hp
        self.base_hp_regen_rate = base_hp_regen_rate
        self.base_stamina_regen_rate = base_stamina_regen_rate

        self.base_stamina = base_stamina
        self.base_strength = base_strength
        self.base_defence = base_defence
        self.base_agility = base_agility
        self.base_dodge = base_dodge
        self.base_accuracy = base_accuracy

        self.base_movement_speed = base_movement_speed
        self.base_dash_distance = base_dash_distance
        self.base_dash_cooldown = base_dash_cooldown
        self.base_dash_duration = base_dash_duration

    def apply_multiplayer(self, playerObject):
        playerObject.max_hp *= self.base_hp
        playerObject.hp_regen_rate *= self.base_hp_regen_rate
        playerObject.max_stamina *= self.base_stamina
        playerObject.stamina_regen_rate *= self.base_stamina_regen_rate

        playerObject.strength *= self.base_strength
        playerObject.defence *= self.base_defence
        playerObject.agility *= self.base_agility

        playerObject.movement_speed *= self.base_movement_speed

        playerObject.dash_distance *= self.base_dash_distance
        playerObject.dash_cooldown *= self.base_dash_cooldown
        playerObject.dash_duration *= self.base_dash_duration

    def character_start_skills(self, playerObject):
        """
        Characters Skills that should be one time applied
        """
        pass

    def character_skills(self, playerObject):
        """
        Character Skills that should be applied every frame
        """
        pass

    def character_variables_modifiers(self, playerObject):
        """
        Static modifiers apply to player
        """
        playerObject.walk_time_interval += playerObject.walk_time_interval * self.base_movement_speed
        playerObject.sprint_time_interval += playerObject.sprint_time_interval * self.base_movement_speed

    def generate_detailed_desc(self, playerObject):
        desc = ""

        # HP and Regeneration
        if self.base_hp != 1:
            hp_modifier = (self.base_hp * 100 - 100)
            sign = "+" if hp_modifier >= 0 else "-"
            desc += f"Hp: {sign}{abs(hp_modifier)}% ({playerObject.max_hp * self.base_hp})\n"
        if self.base_hp_regen_rate != 1:
            regen_modifier = (self.base_hp_regen_rate * 100 - 100)
            sign = "+" if regen_modifier >= 0 else "-"
            desc += f"HP Regen Rate: {sign}{abs(regen_modifier)}%\n"

        # Stamina and Regeneration
        if self.base_stamina != 1:
            stamina_modifier = (self.base_stamina * 100 - 100)
            sign = "+" if stamina_modifier >= 0 else "-"
            desc += f"Stamina: {sign}{abs(stamina_modifier)}% ({playerObject.max_stamina * self.base_stamina})\n"
        if self.base_stamina_regen_rate != 1:
            stamina_regen_modifier = (self.base_stamina_regen_rate * 100 - 100)
            sign = "+" if stamina_regen_modifier >= 0 else "-"
            desc += f"Stamina Regen Rate: {sign}{abs(stamina_regen_modifier)}%\n"

        # Combat Stats
        if self.base_strength != 1:
            strength_modifier = (self.base_strength * 100 - 100)
            sign = "+" if strength_modifier >= 0 else "-"
            desc += f"Strength: {sign}{abs(strength_modifier)}%\n"
        if self.base_defence != 1:
            defence_modifier = (self.base_defence * 100 - 100)
            sign = "+" if defence_modifier >= 0 else "-"
            desc += f"Defence: {sign}{abs(defence_modifier)}%\n"
        if self.base_dodge != 1:
            dodge_modifier = (self.base_dodge * 100 - 100)
            sign = "+" if dodge_modifier >= 0 else "-"
            desc += f"Dodge: {sign}{abs(dodge_modifier)}%\n"
        if self.base_accuracy != 1:
            accuracy_modifier = (self.base_accuracy * 100 - 100)
            sign = "+" if accuracy_modifier >= 0 else "-"
            desc += f"Accuracy: {sign}{abs(accuracy_modifier)}%\n"

        # Movement Stats
        if self.base_movement_speed != 1:
            movement_speed_modifier = (self.base_movement_speed * 100 - 100)
            sign = "+" if movement_speed_modifier >= 0 else "-"
            desc += f"Movement Speed: {sign}{abs(movement_speed_modifier)}%\n"

        # Dash Abilities
        if self.base_dash_distance != 1:
            dash_distance_modifier = (self.base_dash_distance * 100 - 100)
            sign = "+" if dash_distance_modifier >= 0 else "-"
            desc += f"Dash Distance: {sign}{abs(dash_distance_modifier)}%\n"
        if self.base_dash_cooldown != 1:
            dash_cooldown_modifier = (self.base_dash_cooldown * 100 - 100)
            sign = "+" if dash_cooldown_modifier >= 0 else "-"
            desc += f"Dash Cooldown: {sign}{abs(dash_cooldown_modifier)}%\n"
        if self.base_dash_duration != 1:
            dash_duration_modifier = (self.base_dash_duration * 100 - 100)
            sign = "+" if dash_duration_modifier >= 0 else "-"
            desc += f"Dash Duration: {sign}{abs(dash_duration_modifier)}%\n"

        if self.detailed_desc_addition is not None:
            desc += self.detailed_desc_addition

        return desc


class StickMan(Character):
    def __init__(self):
        self.name = "StickMan"
        self.desc = "The most well rounded character with basic skills and powers"
        super().__init__(self.name, self.desc)


class Golem(Character):
    def __init__(self):
        self.name = "Golem"
        self.desc = "The powerful golem with great defence. He is very slow and wonky. His hp takes a long time to regenerate"
        super().__init__(self.name, self.desc, base_hp=2, base_defence=2, base_stamina=0, base_stamina_regen_rate=0,
                         base_hp_regen_rate=0.3,
                         base_movement_speed=0.5, base_agility=0.25, base_dodge=0, base_strength=1.5)
        self.detailed_desc_addition = "Cannot Sprint or Dash or Dodge\nCannot regenerate any stamina"

    def character_skills(self, playerObject):
        playerObject.stamina = 0
        playerObject.dodge = 0


class Warrior(Character):
    def __init__(self):
        self.name = "Warrior"
        self.desc = "The mighty warrior. Have good defence and stamina. He is a bit slow. He is very good close range fighter but he have problems with ranged weapons."
        super().__init__(self.name, self.desc, base_hp=1.25, base_defence=1.75, base_stamina=2,
                         base_stamina_regen_rate=2,
                         base_movement_speed=0.75, base_dash_cooldown=0.75,
                         base_accuracy=0.2, base_dodge=1.25)
        self.detailed_desc_addition = ""


class Ranger(Character):
    def __init__(self):
        self.name = "Ranger"
        self.desc = "The the accurate sniper. Have have high accuracy and dodge. But he is very vulnerable and have no clue how to use close range weapons."
        super().__init__(self.name, self.desc, base_hp=0.5, base_defence=0.5, base_stamina=1.5,
                         base_stamina_regen_rate=1.5,
                         base_movement_speed=1.25, base_dash_distance=2, base_dash_cooldown=0.5, base_dash_duration=0.5,
                         base_accuracy=2, base_dodge=2, base_agility=1.25, base_strength=0)
        self.detailed_desc_addition = "Cannot use close range weapons\n"


class Wizard(Character):
    def __init__(self):
        self.name = "Wizard"
        self.desc = "The the wise wizard. He cast powerful spells. He despise other weapons than spells."
        super().__init__(self.name, self.desc, base_hp=0.75, base_stamina=1.5,
                         base_stamina_regen_rate=1.25,
                         base_movement_speed=1.5,
                         base_dodge=1.25, base_agility=2, base_strength=0, base_accuracy=0)
        self.detailed_desc_addition = "Cannot use close range weapons\nCannot use ranged weapons"
