import math
import random
import arcade
from pyglet.math import Vec2
import enemies
import player as pl
import fight
import characters
import waves

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
MAP_WIDTH = 3950
MAP_HEIGHT = 3530
SCREEN_TITLE = "THE GAME"
CAMERA_SPEED = 0.05  # szybokość z jaką kamera nadąża za graczem od 0 do 1


class GameWindow(arcade.Window):
    def __init__(self, width, height, title, player_object):
        super().__init__(width, height, title, fullscreen=True)
        self.set_vsync(True)
        self.playerObject = player_object

    def on_key_press(self, key, key_modifiers):
        self.playerObject.keys[key] = True

    def on_key_release(self, key, key_modifiers):
        try:
            del self.playerObject.keys[key]
        except:
            pass


class GameView(arcade.View):

    def __init__(self, player_object):
        super().__init__()

        self.camera_speed = None
        self.playerObject = player_object

        self.tile_map = None
        self.scene = None

        self.physics_engine = None
        self.enemy_physics_engine = None

        self.camera = None
        self.gui_camera = None

        self.inventoryView = None

        self.waveManager = None

    def setup(self):
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camera.move_to(
            (self.playerObject.center_x - (SCREEN_WIDTH / 2), self.playerObject.center_y - (SCREEN_HEIGHT / 2)), 1)
        self.gui_camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.tile_map = arcade.load_tilemap("maps/notepad/Notepad.tmx", 2)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Slash")
        self.scene.add_sprite_list("Enemies")
        self.scene.add_sprite_list("EnemiesBars")
        self.scene.add_sprite("Player", self.playerObject)

        self.physics_engine = arcade.PymunkPhysicsEngine(damping=0)
        self.physics_engine.add_sprite(self.playerObject,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="player",
                                       max_horizontal_velocity=1000000,
                                       max_vertical_velocity=1000000)
        self.physics_engine.add_sprite_list(self.scene.get_sprite_list("collision"),
                                            collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)

        self.enemy_physics_engine = arcade.PymunkPhysicsEngine(damping=0)
        self.enemy_physics_engine.add_sprite_list(self.scene.get_sprite_list("Enemies"),
                                                  collision_type="Enemies",
                                                  moment_of_intertia=1000000)

        arcade.enable_timings()

        self.waveManager = waves.WaveManager(5)

        self.waveManager.get_wave(1).add_enemy(enemies.Slime, 10)
        self.waveManager.get_wave(2).add_enemy(enemies.SlimeMedium, 10)
        self.waveManager.get_wave(3).add_enemy(enemies.SlimeBig, 10)
        self.waveManager.get_wave(4).add_enemy(enemies.Slime, 10)
        self.waveManager.get_wave(5).add_enemy(enemies.SlimeMedium, 10)

    def on_draw(self):
        self.clear()
        self.scene.draw(pixelated=True)
        # self.scene.draw_hit_boxes((255, 0, 0), 1, ["Player", "Enemies"])

        self.camera.use()

        for e in self.scene.get_sprite_list("Enemies"):
            e.show_hp()

        self.draw_gui()
        self.playerObject.show_bars()

    def draw_gui(self):
        self.gui_camera.use()
        arcade.load_font("fonts/FirstTimeWriting.ttf")
        fps = arcade.Text(
            str(int(arcade.perf_info.get_fps())),
            SCREEN_WIDTH - 30,
            SCREEN_HEIGHT - 30,
            (0, 0, 0, 150),
            20,
            font_name="First Time Writing!"
        )
        fps.draw()

        time = arcade.Text(
            str(int(self.waveManager.current_wave.time)),
            SCREEN_WIDTH / 2 - 50,
            SCREEN_HEIGHT - 50,
            (0, 0, 0, 150),
            40,
            font_name="First Time Writing!",
            bold=True
        )

        time.draw()

        self.camera.use()

    def shake_camera(self, amplitude):
        shake_direction = random.random() * 2 * math.pi
        # How 'far' to shake
        shake_amplitude = amplitude
        # Calculate a vector based on that
        shake_vector = Vec2(
            math.cos(shake_direction) * shake_amplitude,
            math.sin(shake_direction) * shake_amplitude
        )
        # Frequency of the shake
        shake_speed = 1
        # How fast to damp the shake
        shake_damping = 0.9
        # Do the shake
        self.camera.shake(shake_vector, speed=shake_speed, damping=shake_damping)

    def on_update(self, delta_time):
        print(self.playerObject.center_x, self.playerObject.center_y)
        self.physics_engine.step()
        self.enemy_physics_engine.step()

        self.playerObject.movement(self.camera, CAMERA_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, self.physics_engine)
        self.playerObject.update_player(self)

        for e in self.scene.get_sprite_list("Enemies"):
            try:
                e.update_enemy(self.playerObject, self.enemy_physics_engine, self.scene)
            except:
                self.enemy_physics_engine = arcade.PymunkPhysicsEngine(damping=0)
                self.enemy_physics_engine.add_sprite_list(self.scene.get_sprite_list("Enemies"),
                                                          collision_type="Enemies",
                                                          moment_of_intertia=1000000)

        fight.update(self)

        self.waveManager.update(self.scene)

        if arcade.key.ESCAPE in self.playerObject.keys:
            arcade.exit()

        if arcade.key.K in self.playerObject.keys:
            del self.playerObject.keys[arcade.key.K]
            random.choice(self.scene.get_sprite_list("Enemies")).damage(1)


def main():
    player_object = pl.Player("sprites/player/stickman/player_idle_1.png", 1280 * 2, 1280 * 2, characters.Wizard())
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, player_object)
    start_view = GameView(player_object)
    window.show_view(start_view)
    start_view.setup()
    arcade.run()


if __name__ == "__main__":
    main()
