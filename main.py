import random
import arcade
import enemies
import player as pl
import fight
import gui
import characters

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
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
        self.scene.add_sprite("Player", self.playerObject)

        for i in range(0, 3):
            self.scene.add_sprite("Enemies", enemies.Slime(self.playerObject.center_x + random.randint(-500, 500),
                                                           self.playerObject.center_y + random.randint(-500, 500)))
            self.scene.add_sprite("Enemies", enemies.SlimeMedium(self.playerObject.center_x + random.randint(-500, 500),
                                                                 self.playerObject.center_y + random.randint(-500,
                                                                                                             500)))
            self.scene.add_sprite("Enemies", enemies.SlimeBig(self.playerObject.center_x + random.randint(-500, 500),
                                                              self.playerObject.center_y + random.randint(-500, 500)))

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

    def on_draw(self):
        self.clear()
        self.scene.draw(pixelated=True)
        # self.scene.draw_hit_boxes((255, 0, 0), 1, ["Player", "Enemies"])
        self.scene.get_sprite_list("Slash").visible = False

        self.camera.use()

        for e in self.scene.get_sprite_list("Enemies"):
            e.show_hp()

        # self.draw_gui()
        self.playerObject.show_bars()

    def draw_gui(self):
        self.gui_camera.use()
        self.camera.use()

    def on_update(self, delta_time):
        self.physics_engine.step()
        self.enemy_physics_engine.step()

        self.playerObject.movement(self.camera, CAMERA_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, self.physics_engine)
        self.playerObject.update_player(self.physics_engine)

        for e in self.scene.get_sprite_list("Enemies"):
            try:
                e.update_enemy(self.playerObject, self.enemy_physics_engine, self.scene)
            except:
                self.enemy_physics_engine = arcade.PymunkPhysicsEngine(damping=0)
                self.enemy_physics_engine.add_sprite_list(self.scene.get_sprite_list("Enemies"),
                                                          collision_type="Enemies",
                                                          moment_of_intertia=1000000)

        fight.update(self.playerObject, self.physics_engine, self.scene)

        if arcade.key.ESCAPE in self.playerObject.keys:
            arcade.exit()

        if arcade.key.K in self.playerObject.keys:
            del self.playerObject.keys[arcade.key.K]
            self.scene.get_sprite_list("Enemies")[0].damage(10000)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == 1:
            fight.get_slash(self.playerObject, self.scene, x, y, self.playerObject.strength, 10, 0.2)


def main():
    player_object = pl.Player("sprites/player/stickman/player_idle_1.png", 1280 * 2, 1280 * 2, characters.Wizard())
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, player_object)
    start_view = GameView(player_object)
    window.show_view(start_view)
    start_view.setup()
    arcade.run()


if __name__ == "__main__":
    main()
