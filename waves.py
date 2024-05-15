import random
import arcade

import score
import shop
import sound

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.window_commands.get_display_size()
if not SCREEN_WIDTH == 1920 and not SCREEN_HEIGHT == 1080:
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
DEFAULT_COOLDOWN = 3


class WaveManager:
    def __init__(self,gameView, waves_count, spawn_cooldown_change=0.25):
        self.waves_count = waves_count
        self.waves = [None]
        for i in range(0, waves_count):
            cooldown = DEFAULT_COOLDOWN - i * spawn_cooldown_change
            if cooldown < 0:
                cooldown = 0.5
            self.waves.append(Wave(cooldown))
        self.current_wave = self.waves[1]
        self.current_wave_number = 1
        self.gameView = gameView

    def get_wave(self, number):
        return self.waves[number]

    def update(self, scene):
        self.current_wave.update(scene)
        if self.current_wave.completed:
            try:
                self.current_wave_number += 1
                self.current_wave = self.waves[self.current_wave_number]
                self.gameView.window.show_view(shop.ShopView(self.gameView))
            except IndexError:
                self.gameView.window.show_view(score.WinScreen(self.gameView))

    def draw_wave_status(self):
        if self.current_wave.count_down > 1:
            wave = arcade.Text(
                f"WAVE: {self.current_wave_number}/{self.waves_count}",
                SCREEN_WIDTH / 2 - 150,
                SCREEN_HEIGHT - 50,
                (0, 0, 0, 200),
                40,
                font_name="First Time Writing!",
                bold=True
            )
            wave.draw()
            time = arcade.Text(
                f"begins in {int(round(self.current_wave.count_down, 0))}",
                SCREEN_WIDTH / 2 - 130,
                SCREEN_HEIGHT - 125,
                (0, 0, 0, 200),
                40,
                font_name="First Time Writing!",
                bold=True,
            )

            time.draw()
        else:
            time = arcade.Text(
                str(int(self.current_wave.time)),
                SCREEN_WIDTH / 2 - 50,
                SCREEN_HEIGHT - 125,
                (0, 0, 0, 200),
                40,
                font_name="First Time Writing!",
                bold=True
            )

            time.draw()
            wave = arcade.Text(
                f"WAVE: {self.current_wave_number}/{self.waves_count}",
                SCREEN_WIDTH / 2 - 150,
                SCREEN_HEIGHT - 50,
                (0, 0, 0, 200),
                40,
                font_name="First Time Writing!",
                bold=True
            )
            wave.draw()


class Wave:
    def __init__(self, cooldown_spawn):
        self.time = 60
        self.enemies = []
        self._default_enemy_cooldown_spawner = cooldown_spawn
        self.enemy_cooldown_spawner = 0
        self.completed = False
        self.count_down = 5

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def update(self, scene):
        if self.count_down >= 1:
            self.count_down -= 1/60
        elif not self.completed:
            self.time -= 1 / 60
            if self.time <= 0 or len(self.enemies) == 0:
                self.end_wave(scene)

            self.enemy_cooldown_spawner -= 1 / 60
            if self.enemy_cooldown_spawner <= 0:
                self.enemy_cooldown_spawner = random.randint(self._default_enemy_cooldown_spawner/2 * 10000, self._default_enemy_cooldown_spawner * 10000) / 10000
                enemy = random.choice(self.enemies)
                playerObject = scene.get_sprite_list("Player")[0]

                min_monster_distance = 150
                max_monster_distance = 400
                margin = 200
                if playerObject.direction_move == "Left":
                    monster_x_offset = -random.randint(min_monster_distance, max_monster_distance)
                    monster_y_offset = random.randint(-margin, margin)
                elif playerObject.direction_move == "Right":
                    monster_x_offset = random.randint(min_monster_distance, max_monster_distance)
                    monster_y_offset = random.randint(-margin, margin)
                elif playerObject.direction_move == "Up":
                    monster_x_offset = random.randint(-margin, margin)
                    monster_y_offset = random.randint(min_monster_distance, max_monster_distance)
                elif playerObject.direction_move == "UpRight":
                    monster_x_offset = random.randint(min_monster_distance, max_monster_distance)
                    monster_y_offset = random.randint(min_monster_distance, max_monster_distance)
                elif playerObject.direction_move == "UpLeft":
                    monster_x_offset = -random.randint(min_monster_distance, max_monster_distance)
                    monster_y_offset = random.randint(min_monster_distance, max_monster_distance)

                elif playerObject.direction_move == "Down":
                    monster_x_offset = random.randint(-margin, margin)
                    monster_y_offset = -random.randint(min_monster_distance, max_monster_distance)
                elif playerObject.direction_move == "DownRight":
                    monster_x_offset = random.randint(min_monster_distance, max_monster_distance)
                    monster_y_offset = -random.randint(min_monster_distance, max_monster_distance)
                elif playerObject.direction_move == "DownLeft":
                    monster_x_offset = -random.randint(min_monster_distance, max_monster_distance)
                    monster_y_offset = -random.randint(min_monster_distance, max_monster_distance)

                else:
                    monster_x_offset = random.randint(min_monster_distance, max_monster_distance)
                    monster_y_offset = random.randint(min_monster_distance, max_monster_distance)

                x = int(playerObject.center_x) + monster_x_offset
                y = int(playerObject.center_y) + monster_y_offset
                if not (x in range(1170, 3950)):
                    if x > 3950:
                        x = 3900
                    else:
                        x = 1180
                if not (y in range(1075, 3530)):
                    if y > 3530:
                        y = 3500
                    else:
                        y = 1050
                scene.add_sprite("Enemies", enemy(x, y))

    def end_wave(self, scene):
        scene.get_sprite_list("Enemies").clear()
        scene.get_sprite_list("Bullets").clear()
        scene.get_sprite_list("Coins").clear()
        scene.get_sprite_list("Slash").clear()
        self.completed = True
