import random
import arcade

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.window_commands.get_display_size()
DEFAULT_COOLDOWN = 3


class WaveManager:
    def __init__(self, waves_count, spawn_cooldown_change=0.25):
        self.waves_count = waves_count
        self.waves = [None]
        for i in range(0, waves_count):
            cooldown = DEFAULT_COOLDOWN - i * spawn_cooldown_change
            if cooldown < 0:
                cooldown = 0.5
            self.waves.append(Wave(cooldown))
        self.current_wave = self.waves[1]
        self.current_wave_number = 1

    def get_wave(self, number):
        return self.waves[number]

    def update(self, scene):
        self.current_wave.update(scene)
        if self.current_wave.completed:
            try:
                self.current_wave_number += 1
                self.current_wave = self.waves[self.current_wave_number]
            except:
                arcade.exit()

    def draw_wave_status(self):
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
        self.time = 120
        self.enemies = []
        self._default_enemy_cooldown_spawner = cooldown_spawn
        self._enemy_cooldown_spawner = 0
        self.completed = False

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def update(self, scene):
        if not self.completed:
            self.time -= 1 / 60
            if self.time <= 0 or len(self.enemies) == 0:
                self.end_wave(scene)

            self._enemy_cooldown_spawner -= 1 / 60
            if self._enemy_cooldown_spawner <= 0:
                self._enemy_cooldown_spawner = random.randint(self._default_enemy_cooldown_spawner/2 * 10000, self._default_enemy_cooldown_spawner * 10000) / 10000
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
        enemies = scene.get_sprite_list("Enemies")
        for e in enemies:
            e.kill()
        self.completed = True
