import re
import arcade
import gui
import itemDB
import items
import sound

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
        self.tooltip = None

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
        self.itemsToSell = [
            gui.ShopCard(500 + 250, SCREEN_HEIGHT - 225, itemDB.random_util(), self, 0.85),
            gui.ShopCard(SCREEN_WIDTH - 500 - 250, SCREEN_HEIGHT - 225, itemDB.random_item(), self, 0.85),
            gui.ShopCard(500 + 250, SCREEN_HEIGHT / 2, itemDB.random_tool(), self, 0.85),
            gui.ShopCard(SCREEN_WIDTH - 500 - 250, SCREEN_HEIGHT / 2, itemDB.random_tool(), self, 0.85),
            gui.ShopCard(500 + 250, 225, itemDB.random_item(), self, 0.85),
            gui.ShopCard(SCREEN_WIDTH - 500 - 250, 225, itemDB.random_item(), self, 0.85),
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

        self.scene.add_sprite_list("Slots")
        i = 0
        for r in range(0, 3):
            for c in range(0, 6):
                s = gui.Slot(50 + 80 * c, (SCREEN_HEIGHT / 2 - 100) - 80 * r, scale=0.2, index=i)
                self.scene.add_sprite("Slots", s)
                i += 1

        self.scene.add_sprite_list("SlotsW")
        i = 0
        for c in range(0, 4):
            s = gui.Slot(70 + 120 * c, 150, scale=0.3, index=i)
            self.scene.add_sprite("SlotsW", s)
            i += 1

        self.scene.add_sprite_list("Tooltips")

        self.load_inventory()

    def on_draw(self):
        self.clear()
        self.camera.use()

        self.scene.draw()

        self.draw_stats()

        self.draw_shop()

        self.draw_wave()

        if self.tooltip and self.tooltip.slot.item:
            self.tooltip.draw()
            self.tooltip.draw_content()
        else:
            self.tooltip = None

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

        for s in self.scene.get_sprite_list("Slots"):
            s.draw_item()

        for s in self.scene.get_sprite_list("SlotsW"):
            s.draw_item()

    def draw_shop(self):
        shop = arcade.Text(
            f"SHOP",
            SCREEN_WIDTH - 500 - 20,
            SCREEN_HEIGHT - 70,
            (0, 0, 0, 255),
            50,
            font_name="First Time Writing!",
            anchor_x="right"
        )
        shop.draw()

        coin_image = arcade.Sprite("sprites/coin.png", center_x=550, center_y=SCREEN_HEIGHT - 50, scale=1)

        coins = arcade.Text(
            f"{self.playerObject.coins}",
            coin_image.right + 20,
            SCREEN_HEIGHT - 75,
            (0, 0, 0, 255),
            50,
            font_name="First Time Writing!",
            bold=True,
            anchor_x="left"
        )

        coins.draw()
        coin_image.draw()

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
        desc += f"Hp: {round(int(self.playerObject.hp), 2)}/{round(int(self.playerObject.max_hp), 2)}\n"
        desc += f"HP Regen Rate per Second: {round(self.playerObject.hp_regen_rate, 2)}\n"
        desc += f"Stamina: {round(self.playerObject.max_stamina, 2)}\n"
        desc += f"Stamina Regen Rate per Second: {round(self.playerObject.stamina_regen_rate, 2)}\n\n"

        desc += f"Strength  (Mele Damage Multiplier): {round(self.playerObject.strength, 2)}%\n"
        desc += f"Agility  (Wands Damage Multiplier): {round(self.playerObject.agility, 2)}%\n"
        desc += f"Accuracy  (Bows Damage Multiplier): {round(self.playerObject.accuracy, 2)}%\n\n"

        desc += f"Movement Speed: {round(self.playerObject.movement_speed / 100, 2)}\n"
        desc += f"Dash Distance: {round(self.playerObject.dash_distance / 100, 2)}\n"
        desc += f"Dash Cooldown: {round(self.playerObject.dash_cooldown, 2)}s\n\n"

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
        if self.window.current_view is self:
            sound.play_sound("sounds/wave_start.mp3")
            self.window.show_view(self.gameView)
            self.tooltip = None

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        for s in self.scene.get_sprite_list("Slots"):
            if s.is_clicked(x, y) and s.item is not None:
                self.show_tooltip(s)
                break
        for s in self.scene.get_sprite_list("SlotsW"):
            if s.is_clicked(x, y) and s.item is not None:
                self.show_tooltip(s)
                break

    def show_tooltip(self, slot):
        if self.tooltip and slot is self.tooltip.slot:
            self.tooltip = None
            sound.play_random_paper()
        else:
            self.tooltip = gui.ToolTip(slot.right + 64, slot.top + 64, slot, self)
            sound.play_random_paper()

    def load_inventory(self):
        for i in self.scene.get_sprite_list("Slots"):
            i.item = None
            i.image = None

        for w in self.scene.get_sprite_list("SlotsW"):
            w.item = None
            w.image = None

        for i in range(0, len(self.playerObject.inventory)):
            self.scene.get_sprite_list("Slots")[i].add_item(self.playerObject.inventory[i])

        for w in range(0, len(self.playerObject.weapons)):
            self.scene.get_sprite_list("SlotsW")[w].add_item(self.playerObject.weapons[w])

