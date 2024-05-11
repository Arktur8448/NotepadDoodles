import arcade
import arcade.gui
from typing import Tuple

import items

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.window_commands.get_display_size()


class IndicatorBar:
    """
    Bar which can display information about a sprite.

    bar components.
    :param center_x: The initial position x of the bar.
    :param center_y: The initial position y of the bar.
    :param arcade.Color background_sprite: The path to background sprite.
    :param int width: The width of the bar.
    :param int height: The height of the bar.
    :param int border_size: The size of the bar's border.
    """

    def __init__(
            self,
            center_x,
            center_y,
            background_sprite: str = "",
            width: int = 100,
            height: int = 4,
            border_size: int = 4,
    ) -> None:
        # Set the needed size variables
        self._box_width: int = width
        self._box_height: int = height
        self._full_width: int = self._box_width
        self.center_x: float = center_x
        self.center_y: float = center_y
        self._fullness: float = 0.0
        self.border_size = border_size

        # Create the boxes needed to represent the indicator bar
        self._background_box = arcade.load_texture(background_sprite)
        # self._full_box = arcade.load_texture(fullness_sprite)

        # Set the fullness and position of the bar
        self.fullness: float = 1.0

    def draw(self):
        self._background_box.draw_sized(self.center_x, self.center_y, self._box_width + self.border_size,
                                        self._box_height + self.border_size)
        # self._full_box.draw_sized(self.center_x - (self._box_width / 2) + (self._full_width / 2), self.center_y, self._full_width, self._box_height)
        arcade.draw_rectangle_filled(self.center_x - (self._box_width / 2) + (self._full_width / 2), self.center_y,
                                     self._full_width, self._box_height, (0, 0, 0, 100))

    @property
    def fullness(self) -> float:
        """Returns the fullness of the bar."""
        return self._fullness

    @fullness.setter
    def fullness(self, new_fullness: float) -> None:
        """Sets the fullness of the bar."""
        # Check if new_fullness if valid
        if 0.0 <= new_fullness <= 1.0:
            # Set the size of the bar
            self._fullness = new_fullness
            self._full_width = self._box_width * new_fullness
        elif new_fullness < 0:
            self._fullness = 0
            self._full_width = 0

    @property
    def position(self) -> Tuple[float, float]:
        """Returns the current position of the bar."""
        return self.center_x, self.center_y

    @position.setter
    def position(self, new_position: Tuple[float, float]) -> None:
        """Changes the current position of the bar."""
        self.center_x, self.center_y = new_position


class Button(arcade.gui.UITextureButton):
    def __init__(self, width, height, text, font_size=25):
        self.hover_width = width * 1.1
        self.hover_height = height * 1.1
        button = arcade.load_texture("sprites/gui/buttons/button.png")
        button_hover = arcade.load_texture("sprites/gui/buttons/button_hover.png")
        arcade.load_font("fonts/FirstTimeWriting.ttf")
        style = {
            "font_name": "First Time Writing!",
            "font_size": font_size,
            "font_color": arcade.color.BLACK,
        }
        super().__init__(width=width, height=height, texture=button, texture_hovered=button_hover, text=text,
                         style=style)


class CharacterCard:
    def __init__(self, x, y, character,view, desc_font_size_scale=1):
        if SCREEN_WIDTH != 1920 or SCREEN_HEIGHT != 1080:
            self.scale = min(SCREEN_WIDTH / 1920, SCREEN_HEIGHT / 1080) * 1.2
        else:
            self.scale = 1.4
        self.character = character
        self.view = view

        self.border = arcade.Sprite("sprites/card/border.png", center_x=x, center_y=y, scale=1.25 * self.scale)
        self.image = arcade.Sprite(f"sprites/player/{self.character.name.lower()}/player_idle_1.png",
                                   center_x=self.border.left + 42 * self.scale, center_y=self.border.top - 52 * self.scale,
                                   image_height=64, image_width=64, scale=self.scale)

        self.scene = arcade.Scene()
        self.scene.add_sprite_list("All")
        self.scene.add_sprite("All", self.border)
        self.scene.add_sprite("All", self.image)

        self.name = arcade.Text(
            self.character.name,
            self.image.right + 10 * self.scale,
            self.image.center_y - 10 * self.scale,
            color=arcade.color.BLACK,
            font_size=25 * self.scale,
            font_name="First Time Writing!",
            bold=True,
        )
        self.desc = arcade.Text(
            self.character.desc + "\n" + self.character.generate_detailed_desc(),
            x + 5 * self.scale,
            y + 55 * self.scale,
            color=(0, 0, 0, 255),
            font_size=10 * self.scale * desc_font_size_scale,
            font_name="First Time Writing!",
            bold=True,
            anchor_x="center",
            width=self.border.width - 30 * self.scale,
            multiline=True,
        )
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        play = Button(178 * self.scale, 35 * self.scale, "PLAY")
        play.on_click = self.start
        self.manager.add(arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="bottom",
                align_x=self.border.right - play.width - 40,
                align_y=self.border.top - play.height - 20,
                child=play)
        )

    def draw(self):
        self.scene.draw(pixelated=True)
        self.name.draw()
        self.desc.draw()
        self.manager.draw()

    def start(self, event=None):
        self.view.play(self.character)


class ShopCard:
    def __init__(self, x, y, item, view, scale=1.5):
        self.scale = scale
        self.item = item
        self.view = view

        self.border = arcade.Sprite("sprites/card/border.png", center_x=x, center_y=y, scale=1.25 * self.scale)
        self.image = arcade.Sprite(texture=self.item.texture,center_x=self.border.left + 100 * self.scale, center_y=self.border.top - 82 * self.scale,
                                   image_height=128 * self.scale, image_width=128 * self.scale, scale=1.75 * self.scale)

        self.scene = arcade.Scene()
        self.scene.add_sprite_list("All")
        self.scene.add_sprite("All", self.border)
        self.scene.add_sprite("All", self.image)

        self.name = arcade.Text(
            self.item.name,
            self.border.right - 150 * self.scale,
            self.border.top - 60 * self.scale,
            color=arcade.color.BLACK,
            font_size=30 * self.scale,
            font_name="First Time Writing!",
            bold=True,
            anchor_x="center"
        )
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        buy = Button(350 * self.scale, 80 * self.scale, "BUY", font_size=35 * self.scale)
        buy.on_click = self.buy
        self.manager.add(arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="bottom",
                align_x=(self.border.left + self.border.width / 2) - buy.width / 2,
                align_y=self.border.bottom + 20 * self.scale,
                child=buy)
        )

        desc = ""
        if type(self.item) is items.Weapon:
            desc += f"Damage: {self.item.damage}\n"
            desc += f"Speed: {self.item.speed}\n"
            desc += f"Range: {self.item.attack_range}\n"

        elif type(self.item) is items.Wand or type(self.item) is items.RangedWeapon:
            desc += f"Damage: {self.item.damage}\n"
            desc += f"Speed: {self.item.speed}\n"
            desc += f"Range: {self.item.attack_range}\n"
            desc += f"Bullet Speed: {self.item.bullet_speed}\n"

        self.desc = arcade.Text(
            desc,
            self.border.right - 150 * self.scale,
            self.name.bottom - 25 * self.scale,
            color=(0, 0, 0, 255),
            font_size=17 * self.scale,
            font_name="First Time Writing!",
            bold=True,
            width=250 * self.scale,
            multiline=True,
            anchor_x="center",
            align="center"
        )

    def draw(self):
        self.scene.draw(pixelated=True)
        self.name.draw()
        self.manager.draw()
        self.desc.draw()

    def buy(self, event=None):
        if arcade.get_window().current_view is self.view:
            pass