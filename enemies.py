import math
import random
import arcade
import gui
import misc
import fight


class Enemy(arcade.Sprite):
    def __init__(self, name, pos_x, pos_y, min_coin_drop=0, max_coin_drop=0, hp=1, move_speed=1.0,
                 attack_damage=1.0, attack_cooldown=1.0, drop=None):
        super().__init__(filename=f"sprites/enemies/{name.lower()}/{name.lower()}_base.png", center_x=pos_x,
                         center_y=pos_y, scale=1)
        self.name = name

        self.hp = hp
        self.max_hp = self.hp

        self.move_speed = move_speed * 3000

        self.coin_drop = random.randint(min_coin_drop, max_coin_drop)
        self.drop = drop if drop else []

        self._load_textures()
        self.ifAttack = False
        self.ifMoving = False

        self.move_time_interval = 1
        self._cur_texture = 1
        self._time_counter = 0

        self._alpha_counter = 255
        self.playHitAnimation = False

        self.direction_move = "Right"

        self.modify_bar_pos_y = 0.6
        self.modify_bar_scale = 0.75

        self.scene = None

        self._time_move_counter = -1
        self._optimization_time = 5
        self._move_force = (0, 0)

        self.distance = None

        self.attack_cooldown = attack_cooldown
        self._attack_cooldown_counter = self.attack_cooldown
        self.canAttack = False

        self.attack_damage = attack_damage

    def _load_textures(self):
        self.move_left = []
        for i in range(1, 32):
            try:
                self.move_left.append(
                    arcade.load_texture(f"sprites/enemies/{self.name.lower()}/{self.name.lower()}_walk_{i}.png"))
            except FileNotFoundError:
                break
        self.move_right = []
        for i in range(1, 6):
            try:
                self.move_right.append(
                    arcade.load_texture(f"sprites/enemies/{self.name.lower()}/{self.name.lower()}_walk_{i}.png",
                                        flipped_horizontally=True))
            except FileNotFoundError:
                break

        self.move_animation_count = len(self.move_right)
        self.idle_texture = arcade.load_texture(f"sprites/enemies/{self.name.lower()}/{self.name.lower()}_base.png")
        self.idle_texture_flip = arcade.load_texture(
            f"sprites/enemies/{self.name.lower()}/{self.name.lower()}_base.png", flipped_horizontally=True)

    def update_enemy(self, gameView):
        self.scene = gameView.scene
        playerObject = gameView.playerObject
        physics_engine = gameView.enemy_physics_engine

        if self._attack_cooldown_counter <= 0:
            self._attack_cooldown_counter = 0
            self.canAttack = True
        else:
            self._attack_cooldown_counter -= 1 / 60

        self.distance = ((playerObject.center_x - self.center_x) ** 2 + (
                playerObject.center_y - self.center_y) ** 2) ** 0.5

        self.attack_player(gameView)

        self.move_to_player(playerObject, physics_engine)

        def _update_animation(delta_time: float = 1 / 60):
            if self.ifAttack:
                self._cur_texture = 0
                # self.direction_move = self.direction_attack
            elif self.ifMoving:
                self._time_counter += delta_time
                if self._time_counter >= self.move_time_interval:
                    self._cur_texture += 1
                    self._time_counter = 0
                if self._cur_texture > self.move_animation_count - 1:
                    self._cur_texture = 0

                if self.direction_move == "Right":
                    self.texture = self.move_right[self._cur_texture]
                else:
                    self.texture = self.move_left[self._cur_texture]
            else:
                if self.direction_move == "Right":
                    self.texture = self.idle_texture_flip
                else:
                    self.texture = self.idle_texture

            def _hit_animation():
                self.color = (255, 255, 255, self._alpha_counter)
                self._alpha_counter -= 20
                if self._alpha_counter < 70:
                    self.playHitAnimation = False
                    self._alpha_counter = 255
                    self.color = (255, 255, 255, 255)

            if self.playHitAnimation:
                _hit_animation()

        _update_animation()

        if self.hp <= 0:
            self.die(gameView.scene)

    def move_to_player(self, playerObject, physics_engine):
        """Move behaviour"""

    def damage(self, hp):
        self.hp -= hp
        self.playHitAnimation = True

    def attack_player(self, gameView):
        """Attack Behaviour"""

    def die(self, scene):
        self.die_effect()
        while self.coin_drop > 0:
            if self.coin_drop - 50 >= 0:
                scene.add_sprite("Coins", misc.Coin(50, self.center_x, self.center_y))
                self.coin_drop -= 50
            elif self.coin_drop - 20 >= 0:
                scene.add_sprite("Coins", misc.Coin(20, self.center_x, self.center_y))
                self.coin_drop -= 20
            elif self.coin_drop - 10 >= 0:
                scene.add_sprite("Coins", misc.Coin(10, self.center_x, self.center_y))
                self.coin_drop -= 10
            elif self.coin_drop - 5 >= 0:
                scene.add_sprite("Coins", misc.Coin(5, self.center_x, self.center_y))
                self.coin_drop -= 5
            elif self.coin_drop - 1 >= 0:
                scene.add_sprite("Coins", misc.Coin(1, self.center_x, self.center_y))
                self.coin_drop -= 1
        self.kill()

    def die_effect(self):
        pass

    def show_hp(self):
        if self.hp != self.max_hp:
            hp_bar = gui.IndicatorBar(self.center_x, self.center_y - 70 * self.modify_bar_pos_y,
                                      "sprites/gui/bars/Bar.png",
                                      100 * self.modify_bar_scale, 16 * self.modify_bar_scale,
                                      2 * self.modify_bar_scale)
            hp_bar.fullness = self.hp / self.max_hp
            hp_bar.draw()


class CloseRangeEnemy(Enemy):
    def __init__(self, name, pos_x, pos_y,
                 min_coin_drop=0, max_coin_drop=0,
                 hp=1, move_speed=1.0,
                 attack_damage=1, attack_cooldown=1,
                 drop=None):
        super().__init__(name, pos_x, pos_y, min_coin_drop, max_coin_drop, hp, move_speed,
                         attack_damage, attack_cooldown, drop)

    def attack_player(self, gameView):
        if self.collides_with_sprite(gameView.playerObject):
            if self.canAttack:
                self.canAttack = False
                self._attack_cooldown_counter = self.attack_cooldown
                gameView.playerObject.damage(self.attack_damage)

    def move_to_player(self, playerObject, physics_engine):
        self._time_move_counter = 0
        self.ifMoving = True
        self._time_move_counter -= 1 / 60
        if int(self._time_move_counter) % 2 == 0 and self.distance > 15:
            if self.distance < 500:
                self._time_move_counter = 0

            if self._time_move_counter <= 0:
                self._time_move_counter = self._optimization_time
                delta_y = playerObject.center_y - self.center_y
                delta_x = playerObject.center_x - self.center_x

                if abs(delta_y) > abs(delta_x):
                    if delta_y > 0:
                        self._move_force = (0, self.move_speed)
                    elif delta_y < 0:
                        self._move_force = (0, -self.move_speed)
                else:
                    if delta_x > 0:
                        self._move_force = (self.move_speed, 0)
                        self.direction_move = "Left"
                    elif delta_x < 0:
                        self._move_force = (-self.move_speed, 0)
                        self.direction_move = "Right"

        physics_engine.apply_force(self, self._move_force)


class Bullet(arcade.Sprite):
    def __init__(self, sprite, bullet_speed, damage, distance, startPos):
        super().__init__(filename=sprite, scale=0.5)
        self.position = startPos
        self.start_pos = self.position
        self.change_x = bullet_speed * 10
        self.change_y = bullet_speed * 10
        self.distance = distance
        self.bullet_speed = bullet_speed
        self.damage = damage

    def move(self, scene, delta_time: float = 1 / 60):
        self.position = (
            self.center_x + self.change_x * delta_time,
            self.center_y + self.change_y * delta_time,
        )
        if arcade.get_distance(self.center_x, self.center_y, self.start_pos[0], self.start_pos[1]) > self.distance:
            self.kill()
        if arcade.check_for_collision(self, scene.get_sprite_list("Player")[0]):
            scene.get_sprite_list("Player")[0].damage(self.damage)
            self.kill()

    def shoot(self, pos):
        x, y = pos
        diff_x = x - self.center_x
        diff_y = y - self.center_y
        angle = math.atan2(diff_y, diff_x)
        angle_deg = math.degrees(angle)
        if angle_deg < 0:
            angle_deg += 360
        self.angle = angle_deg

        self.change_x = math.cos(angle) * self.bullet_speed
        self.change_y = math.sin(angle) * self.bullet_speed


class LongRangeEnemy(Enemy):
    def __init__(self, name, pos_x, pos_y,
                 min_coin_drop=0, max_coin_drop=0,
                 hp=1, move_speed=1.0,
                 attack_damage=1, attack_cooldown=1, attack_range=1, bullet_speed=1.0, bullet_texture=None,
                 drop=None):
        super().__init__(name, pos_x, pos_y, min_coin_drop, max_coin_drop, hp, move_speed,
                         attack_damage, attack_cooldown, drop)
        self.attack_range = attack_range * 300
        self.bullet_texture = bullet_texture
        self.bullet_speed = bullet_speed

    def attack_player(self, gameView):
        if self.distance <= self.attack_range:
            if self.canAttack:
                self.canAttack = False
                self._attack_cooldown_counter = self.attack_cooldown
                b = Bullet(self.bullet_texture, 300 * self.bullet_speed, self.attack_damage, self.attack_range * 1.5,
                           self.position)
                b.shoot(gameView.playerObject.position)
                gameView.scene.add_sprite("Bullets", b)

    def move_to_player(self, playerObject, physics_engine):
        self._time_move_counter = 0
        self._time_move_counter -= 1 / 60
        if int(self._time_move_counter) % 2 == 0:
            if self.distance < 500:
                self._time_move_counter = 0

            if self._time_move_counter <= 0:
                self._time_move_counter = self._optimization_time
                delta_y = playerObject.center_y - self.center_y
                delta_x = playerObject.center_x - self.center_x

                if abs(delta_y) > abs(delta_x):
                    if delta_y > 0:
                        self._move_force = (0, self.move_speed)
                    elif delta_y < 0:
                        self._move_force = (0, -self.move_speed)
                else:
                    if delta_x > 0:
                        self._move_force = (self.move_speed, 0)
                        self.direction_move = "Left"
                    elif delta_x < 0:
                        self._move_force = (-self.move_speed, 0)
                        self.direction_move = "Right"
        else:
            self.ifMoving = False
        if self.distance > self.attack_range * 0.75:
            self.ifMoving = True
            physics_engine.apply_force(self, self._move_force)


class Slime(CloseRangeEnemy):
    def __init__(self, pos_x, pos_y):
        super().__init__(name="slime", pos_x=pos_x, pos_y=pos_y, min_coin_drop=4, max_coin_drop=5, hp=5,
                         move_speed=1.5,
                         attack_damage=5)
        self.move_time_interval = 0.2
        self.scale = 0.8
        self.modify_bar_pos_y = 0.4


class SlimeMedium(CloseRangeEnemy):
    def __init__(self, pos_x, pos_y):
        super().__init__(name="slime", pos_x=pos_x, pos_y=pos_y, min_coin_drop=8, max_coin_drop=10, hp=10,
                         move_speed=1.25,
                         attack_damage=7, attack_cooldown=1.5)
        self.move_time_interval = 0.2
        self.scale = 1.25

    def die_effect(self):
        self.scene.add_sprite("Enemies", Slime(self.center_x + 20, self.center_y + 20))
        self.scene.add_sprite("Enemies", Slime(self.center_x - 20, self.center_y - 20))


class SlimeBig(CloseRangeEnemy):
    def __init__(self, pos_x, pos_y):
        super().__init__(name="slime", pos_x=pos_x, pos_y=pos_y, min_coin_drop=15, max_coin_drop=20, hp=20,
                         move_speed=0.75,
                         attack_damage=12, attack_cooldown=2)
        self.move_time_interval = 0.2
        self.scale = 1.5
        self.modify_bar_pos_y = 0.7

    def die_effect(self):
        self.scene.add_sprite("Enemies", SlimeMedium(self.center_x + 20, self.center_y + 20))
        self.scene.add_sprite("Enemies", SlimeMedium(self.center_x - 20, self.center_y - 20))


class Skeleton(CloseRangeEnemy):
    def __init__(self, pos_x, pos_y):
        super().__init__(name="skeleton", pos_x=pos_x, pos_y=pos_y, min_coin_drop=8, max_coin_drop=10, hp=10,

                         move_speed=1.25,
                         attack_damage=7)
        self.move_time_interval = 0.5


class SkeletonArcher(LongRangeEnemy):
    def __init__(self, pos_x, pos_y):
        super().__init__(name="skeleton_archer", pos_x=pos_x, pos_y=pos_y, min_coin_drop=8, max_coin_drop=10, hp=10,
                         move_speed=1.25,
                         attack_damage=7, attack_cooldown=1.5,
                         attack_range=2, bullet_speed=1.5, bullet_texture="sprites/items/weapons/bullets/arrow.png")
        self.move_time_interval = 0.5
