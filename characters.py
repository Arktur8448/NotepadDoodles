class Character:
    def __init__(self, name="", desc="",
                 base_hp=1, base_hp_regen_rate=1, base_stamina=1, base_stamina_regen_rate=1,
                 base_strenght=1, base_defence=1, base_agility=1,
                 base_movement_speed=1, base_sprint_speed=1,
                 base_dash_distance=1, base_dash_cooldown=1, base_dash_duration=1):
        self.name = name
        self.desc = desc
        self.detailed_desc_addition = None

        # Base stats Multiplayers
        self.base_hp = base_hp
        self.base_hp_regen_rate = base_hp_regen_rate
        self.base_stamina_regen_rate = base_stamina_regen_rate
        self.base_stamina = base_stamina
        self.base_strenght = base_strenght
        self.base_defence = base_defence
        self.base_agility = base_agility
        self.base_movement_speed = base_movement_speed
        self.base_sprint_speed = base_sprint_speed
        self.base_dash_distance = base_dash_distance
        self.base_dash_cooldown = base_dash_cooldown
        self.base_dash_duration = base_dash_duration

    def apply_mulitplayers(self, playerObject):
        playerObject.max_hp *= self.base_hp
        playerObject.hp_regen_rate *= self.base_hp_regen_rate
        playerObject.max_stamina *= self.base_stamina
        playerObject.stamina_regen_rate *= self.base_stamina_regen_rate

        playerObject.strength *= self.base_strenght
        playerObject.defence *= self.base_defence
        playerObject.agility *= self.base_agility

        playerObject.movement_speed *= self.base_movement_speed
        playerObject.sprint_speed *= self.base_sprint_speed

        playerObject.dash_distance *= self.base_dash_distance
        playerObject.dash_cooldown *= self.base_dash_cooldown
        playerObject.dash_duration *= self.base_dash_duration

    def chracter_start_skills(self, playerObject):
        """
        Chracters Skills that should be one time upplied
        """
        pass

    def chracter_skills(self, playerObject):
        """
        Character Skills that should be upplied every frame
        """
        pass

    def generate_detailed_desc(self, playerObject):
        desc = ""
        # Hp and Regeneration
        if self.base_hp != 1:
            desc += f"Hp: {self.base_hp*100}% ({playerObject.max_hp * self.base_hp})\n"
        if self.base_hp_regen_rate != 1:
            desc += f"HP Regen Rate: {self.base_hp_regen_rate * 100}%\n"

        # Stamina and Regeneration
        if self.base_stamina != 1:
            desc += f"Stamina: {self.base_stamina} ({playerObject.max_stamina * self.base_stamina})\n"
        if self.base_stamina_regen_rate != 1:
            desc += f"Stamina Regen Rate: {self.base_stamina_regen_rate * 100}%\n"

        # Combat Stats
        if self.base_strenght != 1:
            desc += f"Strength: {self.base_strenght * 100}%\n"
        if self.base_defence != 1:
            desc += f"Defence: {self.base_defence * 100}%\n"
        if self.base_agility != 1:
            desc += f"Agility: {self.base_agility * 100}%\n"

        # Movement Stats
        if self.base_movement_speed != 1:
            desc += f"Movement Speed: {self.base_movement_speed * 100}%\n"
        if self.base_sprint_speed != 1:
            desc += f"Sprint Speed: {self.base_sprint_speed * 100}%\n"

        # Dash Abilities
        if self.base_dash_distance != 1:
            desc += f"Dash Distance: {self.base_dash_distance * 100}%\n"
        if self.base_dash_cooldown != 1:
            desc += f"Dash Cooldown: {self.base_dash_cooldown * 100}%\n"
        if self.base_dash_duration != 1:
            desc += f"Dash Duration: {self.base_dash_duration * 100}%\n"
        if self.detailed_desc_addition is not None:
            desc += self.detailed_desc_addition
        return desc


class StickMan(Character):
    def __init__(self):
        self.name = "StickMan"
        self.desc = "The most well rounded chracter with basic skills and powers"
        super().__init__(self.name, self.desc)


class Golem(Character):
    def __init__(self):
        self.name = "Golem"
        self.desc = "The powerfull golem with great defence. He is very slow and wonky. His hp takes a long time to regenerate"
        super().__init__(self.name, self.desc, base_hp=2, base_defence=2, base_stamina=0, base_stamina_regen_rate=0, base_hp_regen_rate=0.3, base_movement_speed=0.5)
        self.detailed_desc_addition = "Cannot Sprint or Dash \n"

    def chracter_start_skills(self, playerObject):
        playerObject.walk_time_interval = 1
