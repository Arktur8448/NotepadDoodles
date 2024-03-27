import math
import random
import arcade
from pyglet.math import Vec2
import enemies
import player as pl
import fight
import characters
import waves
import arcade.gui
import gui

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.window_commands.get_display_size()
MAP_WIDTH = 3950
MAP_HEIGHT = 3530
MAP_START_WIDTH = 1170
MAP_START_HEIGHT = 1075
SCREEN_TITLE = "THE GAME"
CAMERA_SPEED = 0.05  # szybokość z jaką kamera nadąża za graczem od 0 do 1
BG_COLOR = (248, 245, 226)


class GameWindow(arcade.Window):
    def __init__(self, width, height, title, player_object):
        super().__init__(width, height, title, fullscreen=True, antialiasing=True)
        self.set_vsync(True)
        self.playerObject = player_object
        arcade.load_font("fonts/FirstTimeWriting.ttf")

    def on_key_press(self, key, key_modifiers):
        self.playerObject.keys[key] = True

    def on_key_release(self, key, key_modifiers):
        try:
            del self.playerObject.keys[key]
        except:
            pass
        if key == arcade.key.O:
            print(arcade.get_scaling_factor(self))


class GameView(arcade.View):

    def __init__(self, main_menu_view):
        super().__init__()

        self.camera_speed = None
        self.playerObject = self.window.playerObject

        self.tile_map = None
        self.scene = None

        self.physics_engine = None
        self.enemy_physics_engine = None

        self.camera = None
        self.gui_camera = None

        self.inventoryView = None

        self.waveManager = None

        self.main_menu_view = main_menu_view

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
        self.scene.add_sprite_list("Coins")
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
        self.enemy_physics_engine.add_sprite_list(self.scene.get_sprite_list("collision"),
                                                  collision_type="wall",
                                                  body_type=arcade.PymunkPhysicsEngine.STATIC)

        arcade.enable_timings()

        self.waveManager = waves.WaveManager(5)

        self.waveManager.get_wave(1).add_enemy(enemies.Slime)

        self.waveManager.get_wave(2).add_enemy(enemies.Slime)
        self.waveManager.get_wave(2).add_enemy(enemies.SlimeMedium)

        self.waveManager.get_wave(3).add_enemy(enemies.Slime)
        self.waveManager.get_wave(3).add_enemy(enemies.SlimeMedium)
        self.waveManager.get_wave(3).add_enemy(enemies.SlimeBig)

        self.waveManager.get_wave(4).add_enemy(enemies.SlimeMedium)
        self.waveManager.get_wave(4).add_enemy(enemies.SlimeBig)

        self.waveManager.get_wave(5).add_enemy(enemies.SlimeBig)

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
        fps = arcade.Text(
            f"FPS:{int(arcade.perf_info.get_fps())}",
            SCREEN_WIDTH - 80,
            SCREEN_HEIGHT - 30,
            (0, 0, 0, 150),
            20,
            font_name="First Time Writing!"
        )
        fps.draw()

        coins = arcade.Text(
            f"{self.playerObject.coins}",
            20,
            SCREEN_HEIGHT - 50,
            (0, 0, 0, 255),
            30,
            font_name="First Time Writing!",
            bold=True
        )
        counter = len(str(self.playerObject.coins))
        coin_image = arcade.Sprite("sprites/coin.png", center_x=60 + (20 * counter), center_y=SCREEN_HEIGHT - 35,
                                   scale=0.8)

        coins.draw()
        coin_image.draw()

        self.waveManager.draw_wave_status()

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
                self.enemy_physics_engine.add_sprite_list(self.scene.get_sprite_list("collision"),
                                                          collision_type="wall",
                                                          body_type=arcade.PymunkPhysicsEngine.STATIC)
        for c in self.scene.get_sprite_list("Coins"):
            c.move(self.playerObject)

        fight.update(self)

        self.waveManager.update(self.scene)

        if arcade.key.K in self.playerObject.keys:
            del self.playerObject.keys[arcade.key.K]
            random.choice(self.scene.get_sprite_list("Enemies")).damage(100)
        if arcade.key.L in self.playerObject.keys:
            del self.playerObject.keys[arcade.key.L]
            self.waveManager.current_wave.completed = True
        if arcade.key.ESCAPE in self.playerObject.keys:
            del self.playerObject.keys[arcade.key.ESCAPE]
            self.window.show_view(PauseView(self))


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.scene = None
        self.camera = None
        self.bg_camera = None
        self.game_view = game_view

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

        resume_button = gui.Button(width=400, height=80, text="Resume")
        self.v_box.add(resume_button.with_space_around(bottom=100))
        resume_button.on_click = self.un_pause

        settings_button = gui.Button(width=400, height=80, text="Settings")
        self.v_box.add(settings_button.with_space_around(bottom=100))

        main_menu_button = gui.Button(width=400, height=80, text="Quit To Main Menu")
        self.v_box.add(main_menu_button.with_space_around(bottom=100))
        main_menu_button.on_click = self.main_menu

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="top",
                align_y=-350,
                child=self.v_box)
        )

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.bg_camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bg_camera.move_to(
            (self.game_view.playerObject.center_x - (SCREEN_WIDTH / 2),
             self.game_view.playerObject.center_y - (SCREEN_HEIGHT / 2)), 1)
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.scene = arcade.Scene()

        self.scene.add_sprite_list("BG")
        lines = arcade.load_texture("maps/notepad/Lines.png")
        for r in range(0, int(SCREEN_HEIGHT / 1.25 / 32)):
            for c in range(0, int(SCREEN_WIDTH / 4 / 32)):
                self.scene.add_sprite("BG", arcade.Sprite(center_x=SCREEN_WIDTH / 2.61 + 32 * c, center_y=SCREEN_HEIGHT - 100 - 32 * r, image_width=32, image_height=32, texture=lines))

    def on_draw(self):
        self.clear()
        self.bg_camera.use()
        self.game_view.scene.draw()
        self.game_view.draw_gui()

        self.camera.use()
        arcade.draw_rectangle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, (0, 0, 0, 150))

        self.scene.draw()

        pause = arcade.Text(
            f"PAUSE",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 200,
            (0, 0, 0, 255),
            80,
            font_name="First Time Writing!",
            anchor_x="center",
        )
        pause.draw()

        self.manager.draw()
        self.bg_camera.use()

    def on_update(self, delta_time):
        if arcade.key.ESCAPE in self.game_view.playerObject.keys:
            del self.game_view.playerObject.keys[arcade.key.ESCAPE]
            self.un_pause()

    def un_pause(self, event=None):
        self.window.show_view(self.game_view)

    def main_menu(self, event=None):
        self.window.show_view(self.game_view.main_menu_view)


class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.scene = None
        self.camera = None
        self.x = 0
        self.y = 0

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

        start_button = gui.Button(width=400, height=80, text="Start")
        self.v_box.add(start_button.with_space_around(bottom=80))
        start_button.on_click = self.start

        settings_button = gui.Button(width=400, height=80, text="Settings")
        self.v_box.add(settings_button.with_space_around(bottom=80))

        quit_button = gui.Button(width=400, height=80, text="Exit")
        self.v_box.add(quit_button.with_space_around(bottom=80))
        quit_button.on_click = self.exit

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="top",
                align_y=-550,
                child=self.v_box)
        )

    def on_show_view(self):
        self.scene = arcade.Scene()
        bg_scale = 0.4
        tile_map = arcade.load_tilemap("maps/notepad/Notepad.tmx", 2 * bg_scale)
        self.scene = arcade.Scene.from_tilemap(tile_map)
        if tile_map.background_color:
            arcade.set_background_color(tile_map.background_color)

        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camera.move_to((60, 460))

    def on_draw(self):
        self.clear()
        self.camera.use()

        self.scene.draw()

        notepad = arcade.Text(
            f"NOTEPAD",
            SCREEN_WIDTH / 2 + 60,
            SCREEN_HEIGHT + 225,
            (0, 0, 0, 255),
            80,
            font_name="First Time Writing!",
            anchor_x="center",
        )
        notepad.draw()

        doodles = arcade.Text(
            f"DOODLES",
            SCREEN_WIDTH / 2 + 60,
            SCREEN_HEIGHT + 50,
            (0, 0, 0, 255),
            110,
            font_name="First Time Writing!",
            anchor_x="center",
            bold=True
        )
        doodles.draw()

        self.manager.draw()

    def start(self, event=None):
        charactersView = CharacterView(self)
        self.window.show_view(charactersView)

    def exit(self, event=None):
        arcade.exit()


class CharacterView(arcade.View):
    def __init__(self, mainMenu):
        super().__init__()
        self.characters = None
        self.mainMenu = mainMenu
        self.scene = None

    def on_show_view(self):
        self.scene = arcade.Scene()
        self.scene.add_sprite_list("BG")
        for r in range(0, int(SCREEN_HEIGHT/64) + 1):
            for c in range(0, int(SCREEN_WIDTH/64) + 1):
                self.scene.add_sprite("BG", arcade.Sprite("maps/notepad/Lines.png", center_x=64*c, center_y=64*r))
        self.characters = [
            gui.CharacterCard(320, SCREEN_HEIGHT - 350, characters.StickMan()),
            gui.CharacterCard(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 350, characters.Golem()),
            gui.CharacterCard(SCREEN_WIDTH - 320, SCREEN_HEIGHT - 350, characters.Warrior()),
            gui.CharacterCard(320, 250, characters.Ranger(), desc_font_size_scale=0.95),
            gui.CharacterCard(SCREEN_WIDTH / 2, 250, characters.Wizard()),
        ]

    def on_draw(self):
        self.clear()
        self.scene.draw()
        for c in self.characters:
            c.draw()

        text = arcade.Text(
            "CHOOSE CHARACTER",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 80,
            (0, 0, 0, 255),
            50,
            font_name="First Time Writing!",
            anchor_x="center",
            bold=True
        )
        text.draw()


def main():
    player_object = pl.Player("sprites/player/stickman/player_idle_1.png", 1280 * 2, 1280 * 2, characters.Wizard())
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, player_object)
    start_view = MainMenuView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
