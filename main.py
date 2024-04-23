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
import json

# pyinstaller --onefile --noconsole --icon=icon.ico main.py
# python -m nuitka --mingw64 main.py --windows-icon-from-ico="icon.ico" --disable-console --onefile --include-data-dir=/fonts --include-data dir=/maps  --include-data dir=/sprites
# TODO
# Abilities
# fast slash
# blind shoot
# boom
# coin throw


SCREEN_WIDTH, SCREEN_HEIGHT = arcade.window_commands.get_display_size()
MAP_WIDTH = 3950
MAP_HEIGHT = 3530
MAP_START_WIDTH = 1170
MAP_START_HEIGHT = 1075
SCREEN_TITLE = "NOTEPAD DOODLES"
CAMERA_SPEED = 0.05  # szybokość z jaką kamera nadąża za graczem od 0 do 1
BG_COLOR = (248, 245, 226)
try:
    with open("SETTINGS.json", 'r') as file:
        settings = json.load(file)
except FileNotFoundError:
    settings = {
        "vsync": False,
        "showFps": False,
    }


class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, fullscreen=True, antialiasing=True, vsync=settings.get("vsync"))
        arcade.load_font("fonts/FirstTimeWriting.ttf")
        self.playerObject = None

    def on_key_press(self, key, key_modifiers):
        try:
            self.playerObject.keys[key] = True
        except:
            pass

    def on_key_release(self, key, key_modifiers):
        try:
            del self.playerObject.keys[key]
        except:
            pass

    def on_resize(self, width: float, height: float):
        global SCREEN_WIDTH, SCREEN_HEIGHT
        SCREEN_WIDTH, SCREEN_HEIGHT = arcade.window_commands.get_display_size()


class GameView(arcade.View):

    def __init__(self, playerObject):
        super().__init__()

        self.camera_speed = None
        self.playerObject = playerObject
        self.window.playerObject = self.playerObject

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
        self.scene.add_sprite_list("Coins")
        self.scene.add_sprite_list("Bullets")
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
        try:
            arcade.enable_timings()
        except:
            pass

        self.waveManager = waves.WaveManager(5, spawn_cooldown_change=-0.25)

        self.waveManager.get_wave(1).add_enemy(enemies.Slime)
        self.waveManager.get_wave(1).add_enemy(enemies.Skeleton)

        self.waveManager.get_wave(2).add_enemy(enemies.Slime)
        self.waveManager.get_wave(2).add_enemy(enemies.SlimeMedium)
        self.waveManager.get_wave(2).add_enemy(enemies.SkeletonArcher)
        self.waveManager.get_wave(2).add_enemy(enemies.Skeleton)

        self.waveManager.get_wave(3).add_enemy(enemies.Skeleton)
        self.waveManager.get_wave(3).add_enemy(enemies.SlimeMedium)
        self.waveManager.get_wave(3).add_enemy(enemies.SlimeBig)
        self.waveManager.get_wave(3).add_enemy(enemies.SkeletonArcher)

        self.waveManager.get_wave(4).add_enemy(enemies.SlimeMedium)
        self.waveManager.get_wave(4).add_enemy(enemies.SlimeBig)
        self.waveManager.get_wave(4).add_enemy(enemies.SkeletonArcher)

        self.waveManager.get_wave(5).add_enemy(enemies.SlimeBig)
        self.waveManager.get_wave(5).add_enemy(enemies.SkeletonArcher)

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
        if settings["showFps"]:
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
        self.playerObject.update_player(self, self.window)

        for e in self.scene.get_sprite_list("Enemies"):
            try:
                e.update_enemy(self)
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

        for b in self.scene.get_sprite_list("Bullets"):
            b.move(self.scene)

        fight.update(self)

        self.waveManager.update(self.scene)
        if arcade.key.ESCAPE in self.playerObject.keys:
            del self.playerObject.keys[arcade.key.ESCAPE]
            self.window.show_view(PauseView(self))

        if 96 in self.playerObject.keys:
            if arcade.key.K in self.playerObject.keys:
                # del self.playerObject.keys[arcade.key.K]
                self.waveManager.current_wave.enemy_cooldown_spawner = 0
            if arcade.key.L in self.playerObject.keys:
                del self.playerObject.keys[arcade.key.L]
                self.waveManager.current_wave.completed = True
            if arcade.key.J in self.playerObject.keys:
                del self.playerObject.keys[arcade.key.J]
                self.playerObject.max_hp = 99999
                self.playerObject.hp = 99999
                self.playerObject.max_stamina = 99999
                self.playerObject.stamina = 99999
                self.playerObject.dash_cooldown = 0
                for w in self.playerObject.weapons:
                    w.speed = 0

        if arcade.key.E in self.playerObject.keys:
            del self.playerObject.keys[arcade.key.E]
            for i in range(0, 20):
                b = fight.Bullet("sprites/coin.png", 300, 1, 600, self.playerObject.position)
                b.shoot({self.playerObject.center_x + random.randint(-500, 500), self.playerObject.center_y + random.randint(-500, 500)})
                self.scene.add_sprite("Bullets", b)


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
        settings_button.on_click = self.show_settings

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
                self.scene.add_sprite("BG", arcade.Sprite(center_x=SCREEN_WIDTH / 2.61 + 32 * c,
                                                          center_y=SCREEN_HEIGHT - 100 - 32 * r, image_width=32,
                                                          image_height=32, texture=lines))

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
        self.window.show_view(MainMenuView())

    def show_settings(self, event=None):
        self.window.show_view(SettingsView(self))


class SettingsView(arcade.View):
    def __init__(self, back_view):
        super().__init__()
        self.manager = None
        self.scene = None
        self.camera = None
        self.back_view = back_view
        if settings["vsync"]:
            self.vsync_text = "X"
        else:
            self.vsync_text = " "
        if settings["showFps"]:
            self.fps_text = "X"
        else:
            self.fps_text = " "

    def generate_buttons(self):
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        back_texture = arcade.load_texture("sprites/gui/buttons/back.png")
        back = arcade.gui.UITextureButton(200, SCREEN_HEIGHT - 200, width=64, height=64, texture=back_texture)
        back.on_click = self.show_back_view
        self.manager.add(arcade.gui.UIAnchorWidget(
            anchor_x="left",
            anchor_y="top",
            align_x=20,
            align_y=-20,
            child=back)
        )

        v_box = arcade.gui.UIBoxLayout()

        vsync_box = arcade.gui.UIBoxLayout(vertical=False)
        vs_text = arcade.gui.UITextArea(text="V-sync",
                                        width=600,
                                        height=125,
                                        font_size=70,
                                        font_name="First Time Writing!",
                                        text_color=arcade.color.BLACK,
                                        )
        vs_button = gui.Button(100, 100, self.vsync_text, font_size=50)
        vs_button.on_click = self.toggle_vsync
        vsync_box.add(vs_text)
        vsync_box.add(vs_button)
        v_box.add(vsync_box.with_space_around(bottom=100))

        fps_box = arcade.gui.UIBoxLayout(vertical=False)
        fps_text = arcade.gui.UITextArea(text="Show FPS",
                                         width=600,
                                         height=125,
                                         font_size=70,
                                         font_name="First Time Writing!",
                                         text_color=arcade.color.BLACK,
                                         )
        fps_button = gui.Button(100, 100, self.fps_text, font_size=50)
        fps_button.on_click = self.toggle_fps
        fps_box.add(fps_text)
        fps_box.add(fps_button)
        v_box.add(fps_box.with_space_around(bottom=100))

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="top",
                align_y=-300,
                child=v_box)
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
        self.generate_buttons()

    def on_draw(self):
        self.clear()
        self.camera.use()

        self.scene.draw()
        text = arcade.Text(
            "SETTINGS",
            SCREEN_WIDTH / 2 + 60,
            SCREEN_HEIGHT * 1.25,
            (0, 0, 0, 255),
            50,
            font_name="First Time Writing!",
            anchor_x="center",
            bold=True
        )
        text.draw()

        self.manager.draw()

    def show_back_view(self, event=None):
        self.window.show_view(self.back_view)

    def toggle_vsync(self, event=None):
        if self.vsync_text == "X":
            self.vsync_text = ""
            self.window.set_vsync(False)
            settings["vsync"] = False
        else:
            self.vsync_text = "X"
            self.window.set_vsync(True)
            settings["vsync"] = True
        self.generate_buttons()
        self.save_settings()

    def toggle_fps(self, event=None):
        if self.fps_text == "X":
            self.fps_text = ""
            settings["showFps"] = False
        else:
            self.fps_text = "X"
            settings["showFps"] = True
        self.generate_buttons()
        self.save_settings()

    def save_settings(self):
        with open("SETTINGS.json", 'w') as file:
            json.dump(settings, file)


class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.scene = None
        self.camera = None

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

        start_button = gui.Button(width=400, height=80, text="Start")
        self.v_box.add(start_button.with_space_around(bottom=80))
        start_button.on_click = self.start

        settings_button = gui.Button(width=400, height=80, text="Settings")
        self.v_box.add(settings_button.with_space_around(bottom=80))
        settings_button.on_click = self.show_settings

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
        charactersView = CharacterView()
        self.window.show_view(charactersView)

    def exit(self, event=None):
        arcade.exit()

    def show_settings(self, event=None):
        self.window.show_view(SettingsView(self))


class CharacterView(arcade.View):
    def __init__(self):
        super().__init__()
        self.characters = []
        self.scene = None
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        back_texture = arcade.load_texture("sprites/gui/buttons/back.png")
        back = arcade.gui.UITextureButton(200, SCREEN_HEIGHT - 200, width=64, height=64, texture=back_texture)
        back.on_click = self.show_main_menu
        self.manager.add(arcade.gui.UIAnchorWidget(
            anchor_x="left",
            anchor_y="top",
            align_x=20,
            align_y=-20,
            child=back)
        )

    def on_show_view(self):
        self.scene = arcade.Scene()
        self.scene.add_sprite_list("BG")
        for r in range(0, int(SCREEN_HEIGHT / 64) + 1):
            for c in range(0, int(SCREEN_WIDTH / 64) + 1):
                self.scene.add_sprite("BG", arcade.Sprite("maps/notepad/Lines.png", center_x=64 * c, center_y=64 * r))
        self.characters = [
            gui.CharacterCard(320, SCREEN_HEIGHT - 350, characters.StickMan(), self),
            gui.CharacterCard(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 350, characters.Golem(), self),
            gui.CharacterCard(SCREEN_WIDTH - 320, SCREEN_HEIGHT - 350, characters.Warrior(), self),
            gui.CharacterCard(320, 250, characters.Ranger(), self, desc_font_size_scale=0.90),
            gui.CharacterCard(SCREEN_WIDTH / 2, 250, characters.Wizard(), self),
            gui.CharacterCard(SCREEN_WIDTH - 320, 250, characters.Thief(), self),
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
        self.manager.draw()

    def show_main_menu(self, event=None):
        self.window.show_view(MainMenuView())

    def play(self, character):
        gameView = GameView(pl.Player("sprites/player/stickman/player_idle_1.png", 1280 * 2, 1280 * 2, character))
        gameView.setup()
        self.window.show_view(gameView)


def main():
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = MainMenuView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
