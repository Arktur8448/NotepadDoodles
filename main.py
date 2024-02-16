import arcade
import player as pl
import fight
import NPC as npc

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

        self.playerObject = player_object

        self.background = None
        self.scene = None

        self.physics_engine = None

        self.camera = None
        self.gui_camera = None

        self.inventoryView = None

    def setup(self):
        self.background = arcade.load_texture("sprites/bg.png")

        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.gui_camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.scene = arcade.Scene()
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Slash")
        self.scene.add_sprite("Player", self.playerObject)

        self.scene.add_sprite_list("NPC")

        # Utworzenie silnkia fizyki nakładającego kolizje na Walls
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=0)
        self.physics_engine.add_sprite(self.playerObject,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="player",
                                       max_horizontal_velocity=1000000,
                                       max_vertical_velocity=1000000)
        # self.physics_engine.add_sprite_list(self.scene.get_sprite_list("collision"),
        #                                     collision_type="wall",
        #                                     body_type=arcade.PymunkPhysicsEngine.STATIC)
        self.physics_engine.add_sprite_list(self.scene.get_sprite_list("NPC"),
                                            collision_type="NPC",
                                            moment_of_intertia=1000000)

    def on_draw(self):
        """
        Render the screen.
        """
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        self.scene.draw(pixelated=True)
        # self.scene.draw_hit_boxes((255, 0, 0), 1, ["Player", "Slash", "NPC"])
        self.scene.get_sprite_list("Slash").visible = False

        self.camera.use()

        for n in self.scene.get_sprite_list("NPC"):
            bar = n.show_health()
            bar.draw()

        self.draw_gui()

    def draw_gui(self):
        self.gui_camera.use()
        hp = arcade.Text(
            f"HP: {int(self.playerObject.health)}/{self.playerObject.max_health}",
            10,
            SCREEN_HEIGHT - 30,
            arcade.color.BLACK,
            20,
            font_name="Kenney Blocks",
        )
        mana = arcade.Text(
            f"MANA: {int(self.playerObject.mana)}/{self.playerObject.max_mana}",
            10,
            SCREEN_HEIGHT - 60,
            arcade.color.BLACK,
            20,
            font_name="Kenney Blocks",
        )
        stamina = arcade.Text(
            f"STAMINA: {int(self.playerObject.stamina)}/{self.playerObject.max_stamina}",
            10,
            SCREEN_HEIGHT - 90,
            arcade.color.BLACK,
            20,
            font_name="Kenney Blocks",
        )
        arcade.draw_rectangle_filled(150, SCREEN_HEIGHT - 50, 300, 100, (205, 127, 50))
        hp.draw()
        mana.draw()
        stamina.draw()
        self.camera.use()

    def on_update(self, delta_time):
        self.physics_engine.step()
        self.playerObject.movement(self.camera, CAMERA_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, self.physics_engine)
        self.playerObject.update_player(self.physics_engine)
        fight.update(self.playerObject, self.physics_engine, self.scene)

        self.scene.update_animation(delta_time, ["Player"])

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == 1:
            fight.get_slash(self.playerObject, self.scene, x, y, self.playerObject.strength, 10, 0.2, 0.2)


def main():
    player_object = pl.Player("sprites/player/player_idle_1.png", 1000, 500)
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, player_object)
    start_view = GameView(player_object)
    window.show_view(start_view)
    start_view.setup()
    arcade.run()


if __name__ == "__main__":
    main()
