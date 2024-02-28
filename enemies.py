import arcade
import gui


class Enemy(arcade.Sprite):
    def __init__(self, name, pos_x, pos_y, coin_drop=0, hp=1, defence=1, dodge=1, move_speed=1.0, drop=None):
        super().__init__(filename=f"sprites/enemies/{name.lower()}/{name.lower()}_base.png", center_x=pos_x, center_y=pos_y, scale=1)
        self.name = name

        self.hp = hp
        self.max_hp = self.hp

        self.defence = defence
        self.dodge = dodge
        self.move_speed = move_speed * 3000

        self.coin_drop = coin_drop
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

    def show_hp(self):
        hp_bar = gui.IndicatorBar(self.center_x, self.center_y - 70 * self.modify_bar_pos_y,
                                  "sprites/gui/bars/bar_full.png", "sprites/gui/bars/Bar.png",
                                  100 * self.modify_bar_scale, 16 * self.modify_bar_scale, 2 * self.modify_bar_scale)
        hp_bar.fullness = self.hp / self.max_hp
        hp_bar.draw()
        heart = arcade.Sprite("sprites/gui/bars/Heart.png", scale=0.5 * self.modify_bar_scale)
        heart.center_x = self.center_x - 50 * self.modify_bar_scale
        heart.center_y = self.center_y - 65 * self.modify_bar_pos_y
        heart.draw()
        hp = arcade.Text(
            f"{int(self.hp)}/{int(self.max_hp)}",
            self.center_x,
            self.center_y - 75 * self.modify_bar_pos_y,
            arcade.color.BLACK,
            12 * self.modify_bar_scale,
            anchor_x="center",
            bold=True
        )
        hp.draw()

    def _load_textures(self):
        self.move_left = []
        for i in range(1, 6):
            self.move_left.append(
                arcade.load_texture(f"sprites/enemies/{self.name.lower()}/{self.name.lower()}_walk_{i}.png"))
        self.move_right = []
        for i in range(1, 6):
            self.move_right.append(
                arcade.load_texture(f"sprites/enemies/{self.name.lower()}/{self.name.lower()}_walk_{i}.png", flipped_horizontally=True))

        self.move_animation_count = len(self.move_right)
        self.idle_texture = arcade.load_texture(f"sprites/enemies/{self.name.lower()}/{self.name.lower()}_base.png")

    def update_enemy(self, playerObject, physics_engine, scene):
        self.scene = scene

        def move_to_player():
            self.ifMoving = True
            delta_y = playerObject.center_y - self.center_y
            delta_x = playerObject.center_x - self.center_x

            if abs(delta_y) > abs(delta_x):
                if delta_y > 0:
                    physics_engine.apply_force(self, (0, self.move_speed))
                elif delta_y < 0:
                    physics_engine.apply_force(self, (0, -self.move_speed))
            else:
                if delta_x > 0:
                    physics_engine.apply_force(self, (self.move_speed, 0))
                    self.direction_move = "Left"
                elif delta_x < 0:
                    physics_engine.apply_force(self, (-self.move_speed, 0))
                    self.direction_move = "Right"

        move_to_player()

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
            self.die()
        
    def damage(self, hp):
        self.hp -= hp
        self.playHitAnimation = True

    def die(self):
        self.die_effect()
        self.kill()

    def die_effect(self):
        pass
            
        
class Slime(Enemy):
    def __init__(self, pos_x, pos_y):
        super().__init__(name="slime", pos_x=pos_x, pos_y=pos_y, coin_drop=5, hp=5, defence=0, dodge=10, move_speed=1)
        self.name = "Slime"
        self.move_time_interval = 0.2
        self.scale = 0.8
        self.modify_bar_pos_y = 0.4


class SlimeMedium(Enemy):
    def __init__(self, pos_x, pos_y):
        super().__init__(name="slime", pos_x=pos_x, pos_y=pos_y, coin_drop=10, hp=10, defence=1, dodge=5, move_speed=0.75)
        self.name = "Slime"
        self.move_time_interval = 0.2
        self.scale = 1.25

    def die_effect(self):
        self.scene.add_sprite("Enemies", Slime(self.center_x, self.center_y))


class SlimeBig(Enemy):
    def __init__(self, pos_x, pos_y):
        super().__init__(name="slime", pos_x=pos_x, pos_y=pos_y, coin_drop=20, hp=30, defence=2, dodge=3, move_speed=0.6)
        self.name = "Slime"
        self.move_time_interval = 0.2
        self.scale = 1.5
        self.modify_bar_pos_y = 0.7

    def die_effect(self):
        self.scene.add_sprite("Enemies", SlimeMedium(self.center_x, self.center_y))