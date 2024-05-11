import re
import arcade
import gui
import itemDB
import items

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.window_commands.get_display_size()
if not SCREEN_WIDTH == 1920 and not SCREEN_HEIGHT == 1080:
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080


class ShopView(arcade.View):
    def __init__(self, gameView):
        super().__init__()
        self.desc_t = None
        self.gameView = gameView
        self.playerObject = gameView.playerObject
        self.scene = None
        self.camera = None
        self.generate_stats()

        b = gui.Button(350, 100, "START", 40)
        b.on_click = self.next_wave
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        v_box = arcade.gui.UIBoxLayout()
        v_box.add(b)
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="right",
                align_x=-75,
                anchor_y="bottom",
                align_y=20,
                child=v_box)
        )
        self.itemsToSell =[
            gui.ShopCard(500 + 250, SCREEN_HEIGHT - 225, itemDB.random_wand(), self, 0.85),
            gui.ShopCard(SCREEN_WIDTH - 500 - 250, SCREEN_HEIGHT - 225, itemDB.random_wand(), self, 0.85),
            gui.ShopCard(500 + 250, SCREEN_HEIGHT / 2, itemDB.random_weapon(), self, 0.85),
            gui.ShopCard(SCREEN_WIDTH - 500 - 250, SCREEN_HEIGHT / 2, itemDB.random_weapon(), self, 0.85),
            gui.ShopCard(500 + 250, 225, itemDB.random_ranged(), self, 0.85),
            gui.ShopCard(SCREEN_WIDTH - 500 - 250, 225, itemDB.random_ranged(), self, 0.85),
        ]

    def on_show_view(self):
        self.scene = arcade.Scene()
        self.camera = arcade.Camera()
        self.camera.move_to((0, 0), 1)
        self.scene.add_sprite_list("BG")
        lines = arcade.load_texture("maps/notepad/Lines.png")
        for r in range(0, int(SCREEN_HEIGHT / 32)):
            for c in range(0, int(SCREEN_WIDTH / 32)):
                self.scene.add_sprite("BG", arcade.Sprite(center_x=32 * c,
                                                          center_y=SCREEN_HEIGHT - 32 * r, image_width=32,
                                                          image_height=32, texture=lines))
        self.scene.add_sprite_list("Dividers")
        divider = arcade.load_texture("sprites/gui/divider.png")
        for r in range(0, int(SCREEN_HEIGHT / 32)):
            self.scene.add_sprite("Dividers",
                                  arcade.Sprite(center_x=500, center_y=SCREEN_HEIGHT - 100 * r, texture=divider))

        for r in range(0, int(SCREEN_HEIGHT / 32)):
            self.scene.add_sprite("Dividers",
                                  arcade.Sprite(center_x=SCREEN_WIDTH - 500, center_y=SCREEN_HEIGHT - 100 * r,
                                                texture=divider))

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw(pixelated=True)

        self.draw_stats()

        self.draw_shop()

        self.draw_wave()

    def draw_stats(self):
        stats = arcade.Text(
            f"STATS",
            20,
            SCREEN_HEIGHT - 70,
            (0, 0, 0, 255),
            50,
            font_name="First Time Writing!"
        )
        stats.draw()

        self.desc_t.draw()
        inventory = arcade.Text(
            f"INVENTORY",
            20,
            SCREEN_HEIGHT / 2,
            (0, 0, 0, 255),
            50,
            font_name="First Time Writing!"
        )
        inventory.draw()

    def draw_shop(self):
        shop = arcade.Text(
            f"SHOP",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 70,
            (0, 0, 0, 255),
            50,
            font_name="First Time Writing!",
            anchor_x="center"
        )
        shop.draw()
        for i in self.itemsToSell:
            i.draw()

    def draw_wave(self):
        wave = arcade.Text(
            f"Next Wave",
            SCREEN_WIDTH - 250,
            SCREEN_HEIGHT - 70,
            (0, 0, 0, 255),
            50,
            font_name="First Time Writing!",
            anchor_x="center"
        )
        wave.draw()
        waveManager = self.gameView.waveManager
        number = arcade.Text(
            f"{waveManager.current_wave_number} / {waveManager.waves_count}",
            SCREEN_WIDTH - 250,
            SCREEN_HEIGHT - 150,
            (0, 0, 0, 255),
            40,
            font_name="First Time Writing!",
            anchor_x="center"
        )
        number.draw()
        monsters = arcade.Text(
            f"Monsters",
            SCREEN_WIDTH - 250,
            SCREEN_HEIGHT - 270,
            (0, 0, 0, 255),
            45,
            font_name="First Time Writing!",
            anchor_x="center",
        )
        monsters.draw()
        mon = ""
        for m in waveManager.current_wave.enemies:
            class_name = m.__name__
            class_name_with_spaces = re.sub(r'(?<!^)(?=[A-Z])', ' ', class_name)
            mon += f"{class_name_with_spaces}\n\n"
        mon = arcade.Text(
            mon,
            SCREEN_WIDTH - 250,
            SCREEN_HEIGHT - 350,
            (0, 0, 0, 255),
            30,
            font_name="First Time Writing!",
            anchor_x="center",
            multiline=True,
            width=400,
            align="center"
        )
        mon.draw()

        self.manager.draw()

    def generate_stats(self):
        desc = ""
        desc += f"Hp: {self.playerObject.max_hp}\n"
        desc += f"HP Regen Rate per Second: {self.playerObject.hp_regen_rate}\n"
        desc += f"Stamina: {self.playerObject.max_stamina}\n"
        desc += f"Stamina Regen Rate per Second: {self.playerObject.stamina_regen_rate}\n\n"

        desc += f"Strength: {self.playerObject.strength}\n"
        desc += f"Agility: {self.playerObject.agility}\n"
        desc += f"Accuracy: {self.playerObject.accuracy}\n\n"

        desc += f"Movement Speed: {self.playerObject.movement_speed / 100}\n"
        desc += f"Dash Distance: {self.playerObject.dash_distance / 100}\n"
        desc += f"Dash Cooldown: {self.playerObject.dash_cooldown}s\n\n"

        if self.playerObject.character.detailed_desc_addition is not None:
            desc += f"{self.playerObject.character.detailed_desc_addition} \n"

        self.desc_t = arcade.Text(
            desc,
            20,
            SCREEN_HEIGHT - 100,
            color=(0, 0, 0, 255),
            font_size=15,
            font_name="First Time Writing!",
            bold=True,
            width=450,
            multiline=True,
        )

    def next_wave(self, e):
        self.window.show_view(self.gameView)
