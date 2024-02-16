import arcade
import time
from pyglet.math import Vec2

DELTA_TIME = 1/60


class Player(arcade.Sprite):
    def __init__(self, sprite_path, x, y):
        super().__init__(filename=sprite_path, center_x=x, center_y=y, scale=0.8)
        self.movement_speed = 5000
        self.sprint_speed = 10000
        self.max_sprint_speed = 3600
        
        self.dash_distance = 2000
        self.dash_cooldown = 0.1
        self.dash_force = [0, 0]
        self.default_dash_duration = 0.3
        self.dash_duration = 0
        self.dash_last_time = time.perf_counter() - self.dash_cooldown

        self.last_time_slash = 0
        self.slash_cooldown_time = 0

        self.keys = {}

        self.direction_move = "Down"
        self.direction_attack = "Down"
        self.can_move = True
        self.moving = False
        self.ifIdle = True
        self.ifAttack = False

        self.cur_texture = 1
        self.time_counter = 0

        self.idle = []
        for i in range(1, 3):
            self.idle.append(arcade.load_texture(f"sprites/player/player_idle_{i}.png"))
        self.idle_animation_count = len(self.idle)
        self.idle_time_interval = 1

        self.move = []
        for i in range(1, 5):
            self.move.append(arcade.load_texture(f"sprites/player/player_walk_{i}.png"))
        self.move_animation_count = len(self.move)
        self.move_time_interval = 0
        self.sprint_time_interval = 0.3
        self.walk_time_interval = 0.5

        self.health = 25
        self.max_health = 30
        self.can_regen_health = True

        self.mana = 10
        self.max_mana = 30
        self.can_regen_mana = True

        self.stamina = 300
        self.max_stamina = 300
        self.can_regen_stamina = True

        self.strength = 10
        self.defence = 10
        self.agility = 10

    def movement(self, camera, camer_speed, width, height, physics_engine):
        """Pełny Ruch Gracza"""
        def check_move_key():  # aktualizacja pozycji w zależności od naciśniętych klawiszy
            if arcade.key.W in self.keys or arcade.key.A in self.keys or arcade.key.S in self.keys or arcade.key.D in self.keys:
                self.moving = True
            else:
                self.moving = False
            if arcade.key.LSHIFT in self.keys and self.stamina > 0:
                self.move_time_interval = self.sprint_time_interval
                self.can_regen_stamina = False
                speed = self.sprint_speed
                if arcade.key.W in self.keys or arcade.key.A in self.keys or arcade.key.S in self.keys or arcade.key.D in self.keys:
                    self.stamina -= 1/10
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
                if time.perf_counter() - self.dash_last_time > self.dash_cooldown and self.stamina > 10:
                    self.stamina -= 10
                    dash()

        def move_camera_to_player():
            position = Vec2(
                self.center_x - width / 2,
                self.center_y - height / 2
            )
            camera.move_to(position, camer_speed)

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
            move_camera_to_player()

    def update_player(self, physics_engine):
        if self.can_regen_health:
            self.health += DELTA_TIME / 5
        if self.can_regen_mana:
            self.mana += DELTA_TIME * 1
        if self.can_regen_stamina:
            if self.stamina < self.max_stamina / 2:
                self.stamina += DELTA_TIME * 3.5  # wolniejsze ładowanie staminy jeśli zużjesz ją w więcej niz w połowie
            elif self.stamina < self.max_stamina:
                self.stamina += DELTA_TIME * 3

        if self.health > self.max_health:
            self.health = self.max_health
        if self.mana > self.max_mana:
            self.mana = self.max_mana
        if self.stamina > self.max_stamina:
            self.stamina = self.max_stamina

        if self.dash_duration > 0:
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

    def update_animation(self, delta_time: float = 1 / 60):
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
