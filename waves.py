import random
import arcade


class WaveManager:
    def __init__(self, waves_count):
        self.waves_count = waves_count
        self.waves = [None]
        for i in range(0, waves_count):
            self.waves.append(Wave())
        self.current_wave = self.waves[1]
        self._current_wave_number = 1

    def get_wave(self, number):
        return self.waves[number]

    def update(self, scene):
        self.current_wave.update(scene)
        if self.current_wave.completed:
            self._current_wave_number += 1
            self.current_wave = self.waves[self._current_wave_number]


class Wave:
    def __init__(self):
        self.time = 120
        self.enemies = []
        self._default_enemy_cooldown_spawner = 0.5
        self._enemy_cooldown_spawner = 0
        self.width = 3950
        self.height = 3530
        self.completed = False

    def add_enemy(self, enemy, amount):
        self.enemies.append([enemy, amount])

    def update(self, scene):
        if not self.completed:
            self.time -= 1 / 60
            if self.time <= 0 or (len(self.enemies) == 0 and len(scene.get_sprite_list("Enemies")) == 0):
                self.end_wave(scene)

            self._enemy_cooldown_spawner -= 1 / 60
            if self._enemy_cooldown_spawner <= 0 and not (len(self.enemies) == 0):
                self._enemy_cooldown_spawner = self._default_enemy_cooldown_spawner
                enemy = random.choice(self.enemies)
                enemy[1] -= 1
                playerObject = scene.get_sprite_list("Player")[0]
                while True:
                    x = playerObject.center_x + random.randint(-500, 500)
                    y = playerObject.center_y + random.randint(-500, 500)
                    # POPRAWIĆ
                    if (not (x > self.width or x < self.width or x < 250 or x > self.width - 250) and not (y > self.height or y < 250)) or arcade.get_distance(x, y, playerObject.center_x, playerObject.center_y) < 300:
                        break
                scene.add_sprite("Enemies", enemy[0](x, y))
                if enemy[1] == 0:
                    self.enemies.remove(enemy)

    def end_wave(self, scene):
        playerObject = scene.get_sprite_list("Player")[0]
        enemies = scene.get_sprite_list("Enemies")
        for e in enemies:
            playerObject.coins += e.coin_drop
            e.kill()
        for e in self.enemies:
            playerObject.coins += e.coin_drop
        self.completed = True
