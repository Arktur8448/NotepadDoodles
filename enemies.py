import arcade
import gui


class Enemy(arcade.Sprite):
    def __init__(self, name, pos_x, pos_y, coin_drop=0, hp=1, defence=1, dodge=1, move_speed=1, drop=None):
        super().__init__(filename=f"sprites/enemies/{name.lower()}/{name.lower()}_idle_1.png", center_x=pos_x, center_y=pos_y, scale=1)
        self.name = name

        self.hp = hp
        self.max_hp = self.hp

        self.defence = defence
        self.dodge = dodge
        self.move_speed = move_speed

        self.coin_drop = coin_drop
        self.drop = drop if drop else []

        self._load_textures()
        self.ifAttack = False
        self.ifMoving = False

        self.move_time_interval = 1
        self.idle_time_interval = 1
        self.cur_texture = 1
        self.time_counter = 0

    def show_hp(self):
        modify_pos_y = 0.6
        modify_scale = 0.75
        hp_bar = gui.IndicatorBar(self.center_x, self.center_y - 70 * modify_pos_y,
                                  "sprites/gui/bars/bar_full.png", "sprites/gui/bars/Bar.png",
                                  100 * modify_scale, 16 * modify_scale, 2 * modify_scale)
        hp_bar.fullness = self.hp / self.max_hp
        hp_bar.draw()
        heart = arcade.Sprite("sprites/gui/bars/Heart.png", scale=0.5 * modify_scale)
        heart.center_x = self.center_x - 50 * modify_scale
        heart.center_y = self.center_y - 65 * modify_pos_y
        heart.draw()
        hp = arcade.Text(
            f"{int(self.hp)}/{int(self.max_hp)}",
            self.center_x,
            self.center_y - 75 * modify_pos_y,
            arcade.color.BLACK,
            12 * modify_scale,
            anchor_x="center",
            bold=True
        )
        hp.draw()

    def _load_textures(self):
        self.idle = []
        for i in range(1, 5):
            self.idle.append(
                arcade.load_texture(f"sprites/enemies/{self.name.lower()}/{self.name.lower()}_idle_{i}.png"))
        self.idle_animation_count = len(self.idle)

        self.move = []
        for i in range(1, 6):
            self.move.append(
                arcade.load_texture(f"sprites/enemies/{self.name.lower()}/{self.name.lower()}_walk_{i}.png"))
        self.move_animation_count = len(self.move)

    def update_enemy(self):
        self._update_animation()

    def _update_animation(self, delta_time: float = 1 / 60):
        if self.ifAttack:
            self.cur_texture = 0
            # self.direction_move = self.direction_attack
        elif self.ifMoving:
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
 
           
class Slime(Enemy):
    def __init__(self, pos_x, pos_y):
        super().__init__(name="slime", pos_x=pos_x, pos_y=pos_y, coin_drop=10, hp=10, defence=0, dodge=10, move_speed=10)
        self.name = "Slime"
        self.ifMoving = True
        self.move_time_interval = 0.2
        self.idle_time_interval = 0.5
