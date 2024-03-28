import math
import random

import arcade
import time
from pyglet.math import Vec2
import gui
import items

DELTA_TIME = 1 / 60


class Player(arcade.Sprite):
    def __init__(self, sprite_path, x, y, character):
        super().__init__(filename=sprite_path, center_x=x, center_y=y, scale=0.8)
        self.character = character

        self.movement_speed = 5000
        self.sprint_multiplayer = 1.25
        self.max_sprint_speed = 3600

        self.dash_distance = 2000
        self.dash_cooldown = 1
        self.dash_stamina_use = 10

        self.dash_force = [0, 0]
        self.dash_duration = 0

        self.default_dash_duration = 0.3
        self.dash_last_time = time.perf_counter() - self.dash_cooldown
        self.isDashing = False

        self.last_time_slash = 0
        self.slash_cooldown_time = 0

        self.keys = {}

        self.direction_move = "Down"
        self.direction_attack = "Down"
        self.can_move = True
        self.moving = False
        self.ifIdle = True
        self.ifAttack = False

        self.hp = 99999999
        self.max_hp = 100
        self.can_regen_hp = True
        self.hp_regen_rate = 1  # Per second

        self.stamina = 9999999999
        self.max_stamina = 10
        self.can_regen_stamina = True
        self.stamina_regen_rate = 2  # Per second
        self.stamina_sprint_use = 3  # Per second

        self.strength = 100  # Close range
        self.defence = 100  # Defence and change to block damage
        self.agility = 100  # Magic
        self.dodge = 100  # Dodge the damage
        self.accuracy = 100 # Ranged

        self.cur_texture = 1
        self.time_counter = 0
        self._alpha_counter = 255
        self.playHitAnimation = False

        self.idle_time_interval = 1

        self.move_time_interval = 0
        self.sprint_time_interval = 0.3
        self.walk_time_interval = 0.5

        self.weapons = [items.Weapon("sprites/gui/bars/Bar.png", "TOPÓR", damage=10, speed=2, attack_range=1, slash_scale=1.5),
                        items.Weapon("sprites/gui/bars/Bar.png", "Dagger", damage=2, speed=0.5, attack_range=0.75)]

        self.coins = 0

        self.gameView = None

        self._setup_character()

    def movement(self, camera, camera_speed, width, height, physics_engine):
        """Pełny Ruch Gracza"""

        def check_move_key():  # aktualizacja pozycji w zależności od naciśniętych klawiszy
            if arcade.key.W in self.keys or arcade.key.A in self.keys or arcade.key.S in self.keys or arcade.key.D in self.keys:
                self.moving = True
            else:
                self.moving = False
            if arcade.key.LSHIFT in self.keys and self.stamina > 0:
                self.move_time_interval = self.sprint_time_interval
                self.can_regen_stamina = False
                speed = self.movement_speed * self.sprint_multiplayer
                if arcade.key.W in self.keys or arcade.key.A in self.keys or arcade.key.S in self.keys or arcade.key.D in self.keys:
                    self.stamina -= DELTA_TIME * self.stamina_sprint_use
                    if self.stamina < 1:
                        self.stamina = -5  # jeśli zbyt mocno zużyjesz staminę to musisz bardziej odpocząć, przez chwilę ciężej ci złapać oddech
            else:
                speed = self.movement_speed
                self.can_regen_stamina = True
                self.move_time_interval = self.walk_time_interval

            if arcade.key.W in self.keys:
                physics_engine.apply_force(self, (0, speed))
                self.direction_move = "Up"
            elif arcade.key.S in self.keys:
                physics_engine.apply_force(self, (0, -speed))
                self.direction_move = "Down"
            else:
                self.change_y = 0

            if arcade.key.A in self.keys:
                physics_engine.apply_force(self, (-speed, 0))
                if arcade.key.W in self.keys:
                    self.direction_move = "UpLeft"
                elif arcade.key.S in self.keys:
                    self.direction_move = "DownLeft"
                else:
                    self.direction_move = "Left"
            elif arcade.key.D in self.keys:
                physics_engine.apply_force(self, (speed, 0))
                if arcade.key.W in self.keys:
                    self.direction_move = "UpRight"
                elif arcade.key.S in self.keys:
                    self.direction_move = "DownRight"
                else:
                    self.direction_move = "Right"

            if arcade.key.SPACE in self.keys:
                if time.perf_counter() - self.dash_last_time > self.dash_cooldown and self.stamina >= self.dash_stamina_use:
                    self.stamina -= self.dash_stamina_use
                    dash()

        def move_camera_to_player(cameraSpeed):
            position = Vec2(
                self.center_x - width / 2,
                self.center_y - height / 2
            )
            if (arcade.key.A in self.keys or arcade.key.D in self.keys) and not (
                    arcade.key.W in self.keys or arcade.key.S in self.keys):
                cameraSpeed /= 5
            camera.move_to(position, cameraSpeed)

        def dash():
            self.dash_last_time = time.perf_counter()
            self.dash_duration = self.default_dash_duration
            self.dash_force = [0, 0]
            if self.direction_move == "Left":
                self.dash_force = [-self.dash_distance, 0]
            elif self.direction_move == "UpLeft":
                self.dash_force = [-self.dash_distance / 2, self.dash_distance / 2]
            elif self.direction_move == "Up":
                self.dash_force = [0, self.dash_distance]

            elif self.direction_move == "UpRight":
                self.dash_force = [self.dash_distance / 2, self.dash_distance / 2]

            elif self.direction_move == "Right":
                self.dash_force = [self.dash_distance, 0]

            elif self.direction_move == "DownRight":
                self.dash_force = [self.dash_distance / 2, -self.dash_distance / 2]

            elif self.direction_move == "Down":
                self.dash_force = [0, -self.dash_distance]

            elif self.direction_move == "DownLeft":
                self.dash_force = [-self.dash_distance / 2, -self.dash_distance / 2]

            physics_engine.apply_force(self, self.dash_force)

        if self.can_move:
            check_move_key()
        if self.moving or self.isDashing:
            move_camera_to_player(camera_speed)

    def update_player(self, gameView):
        self.character.character_skills(self)
        self.gameView = gameView
        physics_engine = gameView.physics_engine

        if self.can_regen_hp:
            self.hp += DELTA_TIME * self.hp_regen_rate
        if self.can_regen_stamina:
            if self.stamina < self.max_stamina / 2:
                self.stamina += DELTA_TIME * (
                        self.stamina_regen_rate * 0.75)  # wolniejsze ładowanie staminy jeśli zużjesz ją w więcej niz w połowie
            elif self.stamina < self.max_stamina:
                self.stamina += DELTA_TIME * self.stamina_regen_rate

        if self.hp > self.max_hp:
            self.hp = self.max_hp
        if self.stamina > self.max_stamina:
            self.stamina = self.max_stamina

        if self.dash_duration > 0:
            self.isDashing = True
            dash_increment = (self.dash_duration * self.dash_distance) * 2
            if self.dash_force[0]:
                if self.dash_force[0] > 0:
                    self.dash_force[0] += dash_increment
                else:
                    self.dash_force[0] -= dash_increment
            if self.dash_force[1]:
                if self.dash_force[1] > 0:
                    self.dash_force[1] += dash_increment
                else:
                    self.dash_force[1] -= dash_increment
            self.dash_duration -= DELTA_TIME
            physics_engine.apply_force(self, self.dash_force)
        else:
            self.isDashing = False

        def _update_animation(delta_time: float = 1 / 60):
            if self.ifAttack:
                self.cur_texture = 0
                self.direction_move = self.direction_attack
            elif self.moving:
                self.time_counter += delta_time
                if self.time_counter >= self.move_time_interval:
                    self.cur_texture += 1
                    self.time_counter = 0
                if self.cur_texture > self.move_animation_count - 1:
                    self.cur_texture = 0
                self.texture = self.move[self.cur_texture]
            else:
                self.time_counter += delta_time
                if self.time_counter >= self.idle_time_interval:
                    self.cur_texture += 1
                    self.time_counter = 0
                if self.cur_texture > self.idle_animation_count - 1:
                    self.cur_texture = 0
                self.texture = self.idle[self.cur_texture]

            def _hit_animation():
                self.color = (255, 255, 255, self._alpha_counter)
                self._alpha_counter -= 20
                if self._alpha_counter < 70:
                    self.playHitAnimation = False
                    self._alpha_counter = 255
                    self.color = (255, 255, 255, 255)

            if self.playHitAnimation:
                self.playHitAnimation = True
                _hit_animation()

        _update_animation()

    def show_bars(self):
        if self.stamina != self.max_stamina and not self.max_stamina == 0 and not self.stamina < 0:
            stamina_bar = gui.IndicatorBar(self.center_x, self.center_y + 70, "sprites/gui/bars/Bar.png", 80, 14, 2)
            stamina_bar.fullness = self.stamina / self.max_stamina
            stamina_bar.draw()
            piorun = arcade.Sprite("sprites/gui/bars/Piorun.png", scale=0.5)
            piorun.center_x = self.center_x - 42
            piorun.center_y = self.center_y + 70
            piorun.draw()
            stamina = arcade.Text(
                f"{int(self.stamina)}/{int(self.max_stamina)}",
                self.center_x,
                self.center_y + 65,
                arcade.color.BLACK,
                10,
                anchor_x="center",
                font_name="First Time Writing!",
                bold=True
            )
            stamina.draw()
        elif self.stamina < 0:
            stamina_bar = gui.IndicatorBar(self.center_x, self.center_y + 70, "sprites/gui/bars/Bar.png", 80, 14, 2)
            stamina_bar.fullness = 0
            stamina_bar.draw()
            piorun = arcade.Sprite("sprites/gui/bars/Piorun.png", scale=0.5)
            piorun.center_x = self.center_x - 42
            piorun.center_y = self.center_y + 70
            piorun.draw()
            stamina = arcade.Text(
                f"{0}/{int(self.max_stamina)}",
                self.center_x,
                self.center_y + 65,
                arcade.color.BLACK,
                10,
                anchor_x="center",
                font_name="First Time Writing!",
                bold=True
            )
            stamina.draw()
        if self.hp != self.max_hp:
            hp_bar = gui.IndicatorBar(self.center_x, self.center_y - 70,"sprites/gui/bars/Bar.png", 100, 16, 2)
            hp_bar.fullness = self.hp / self.max_hp
            hp_bar.draw()
            heart = arcade.Sprite("sprites/gui/bars/Heart.png", scale=0.5)
            heart.center_x = self.center_x - 50
            heart.center_y = self.center_y - 65
            heart.draw()
            hp = arcade.Text(
                f"{int(self.hp)}/{int(self.max_hp)}",
                self.center_x,
                self.center_y - 75,
                arcade.color.BLACK,
                10,
                anchor_x="center",
                font_name="First Time Writing!",
                bold=True
            )
            hp.draw()

    def _setup_character(self):
        self.character.apply_multiplayer(self)
        self.character.character_start_skills(self)
        self.character.character_variables_modifiers(self)

        self._load_textures()

    def _load_textures(self):
        self.idle = []
        for i in range(1, 3):
            try:
                self.idle.append(
                    arcade.load_texture(f"sprites/player/{self.character.name.lower()}/player_idle_{i}.png"))
            except:
                self.idle.append(arcade.load_texture(f"sprites/player/stickman/player_idle_{i}.png"))
        self.idle_animation_count = len(self.idle)

        self.move = []
        for i in range(1, 5):
            try:
                self.move.append(
                    arcade.load_texture(f"sprites/player/{self.character.name.lower()}/player_walk_{i}.png"))
            except:
                self.move.append(arcade.load_texture(f"sprites/player/stickman/player_walk_{i}.png"))
        self.move_animation_count = len(self.move)

    def damage(self, hp):
        self.hp -= hp
        self.playHitAnimation = True
        self.gameView.shake_camera(2)
