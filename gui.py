import arcade
import arcade.gui
from typing import Tuple


class IndicatorBar:
    """
    Bar which can display information about a sprite.

    bar components.
    :param center_x: The initial position x of the bar.
    :param center_y: The initial position y of the bar.
    :param arcade.Color fullness_sprite: The path to fullness sprite.
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
        self.text = text
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
    def __init__(self, x, y, character, desc_font_size_scale=1):
        self.scale = 1.4
        self.character = character

        self.border = arcade.Sprite("sprites/card/border.png", center_x=x, center_y=y, scale=1.25 * self.scale)
        self.image = arcade.Sprite(f"sprites/player/{self.character.name.lower()}/player_idle_1.png",
                                   center_x=self.border.left + 62 * self.scale, center_y=self.border.top - 52 * self.scale,
                                   image_height=64, image_width=64, scale=self.scale)
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

    def draw(self):
        self.border.draw()
        self.image.draw()
        self.name.draw()
        self.desc.draw()
