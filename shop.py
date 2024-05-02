import arcade
import items

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.window_commands.get_display_size()


class ShopView(arcade.View):
    def __init__(self, gameView):
        super().__init__()
        self.gameView = gameView
        self.playerObject = gameView.playerObject
        self.scene = None
        self.camera = None

    def on_show_view(self):
        self.scene = arcade.Scene()
        self.camera = arcade.Camera()
        self.camera.move_to((SCREEN_WIDTH, 0), 1)
        self.scene.add_sprite_list("BG")
        lines = arcade.load_texture("maps/notepad/Lines.png")
        for r in range(0, int(SCREEN_HEIGHT / 32)):
            for c in range(0, int(SCREEN_WIDTH / 32)):
                self.scene.add_sprite("BG", arcade.Sprite(center_x=SCREEN_WIDTH + 32 * c,
                                                          center_y=SCREEN_HEIGHT - 32 * r, image_width=32,
                                                          image_height=32, texture=lines))

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw()

    def on_update(self, delta_time: float):
        if arcade.key.E in self.playerObject.keys:
            del self.playerObject.keys[arcade.key.E]
            self.window.show_view(self.gameView)
