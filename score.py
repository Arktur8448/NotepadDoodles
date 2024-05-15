import json

import arcade
from pyglet.math import Vec2

import gui
import main
import sound

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.window_commands.get_display_size()
if not SCREEN_WIDTH == 1920 and not SCREEN_HEIGHT == 1080:
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080

ENEMIES_KILL = 0


class WinScreenButton(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("sprites/gui/buttons/button_hover.png", center_x=x, center_y=y, scale=1.15)

    def is_clicked(self, point_x, point_y):
        half_width = self.width / 2
        half_height = self.height / 2
        return (self.center_x - half_width <= point_x <= self.center_x + half_width) and (
                self.center_y - half_height <= point_y <= self.center_y + half_height)


class WinScreen(arcade.View):
    def __init__(self, gameView):
        super().__init__()
        self.total_score = None
        self.gameView = gameView
        self.playerObject = gameView.playerObject
        self.gamViewScene = gameView.scene
        self.gamViewScene.get_sprite_list("Enemies").clear()
        self.gamViewScene.get_sprite_list("Bullets").clear()
        self.gamViewScene.get_sprite_list("Coins").clear()
        self.gamViewScene.get_sprite_list("Slash").clear()

        self.rec_opas = 0
        self.rec_opas_targeted = 150
        self.ifFade = True

        self.Cam = arcade.Camera()
        position = Vec2(
            self.playerObject.center_x - SCREEN_WIDTH / 2,
            self.playerObject.center_y - SCREEN_HEIGHT / 2
        )
        self.Cam.move_to(position)

        self.win = arcade.Text(
            f"WIN",
            self.playerObject.center_x,
            self.playerObject.center_y + SCREEN_HEIGHT / 2 - 150,
            (248, 245, 226),
            200,
            font_name="First Time Writing!",
            bold=True,
            anchor_x="center",
            anchor_y="center",
        )
        self.score = arcade.Text(
            f"SCORE",
            self.playerObject.center_x,
            self.playerObject.center_y + SCREEN_HEIGHT / 2 - 350,
            (248, 245, 226),
            100,
            font_name="First Time Writing!",
            bold=True,
            anchor_x="center",
            anchor_y="center",
        )
        self.score_t = self.generate_score()
        self.button = WinScreenButton(self.playerObject.center_x, self.score_t.bottom - 150)
        self.mainmenuText = arcade.Text(
            f"QUIT",
            self.button.center_x,
            self.button.center_y,
            (248, 245, 226),
            50,
            font_name="First Time Writing!",
            bold=True,
            anchor_x="center",
            anchor_y="center"
        )

        self.save_score()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.button.is_clicked(self.playerObject.center_x - SCREEN_WIDTH / 2 + x, self.playerObject.center_y - SCREEN_HEIGHT / 2 + y):
            self.window.show_view(main.MainMenuView())
            sound.play_random_paper()

    def on_draw(self):
        self.clear()
        self.Cam.use()
        if self.ifFade:
            self.gamViewScene.draw(pixelated=True)
            arcade.draw_rectangle_filled(self.playerObject.center_x, self.playerObject.center_y, SCREEN_WIDTH,
                                         SCREEN_HEIGHT + 200, (0, 0, 0, self.rec_opas))
            self.rec_opas += 1
            if self.rec_opas >= self.rec_opas_targeted:
                self.ifFade = False
                sound.play_sound("sounds/win.mp3")

        else:
            self.gamViewScene.draw(pixelated=True)
            arcade.draw_rectangle_filled(self.playerObject.center_x, self.playerObject.center_y, SCREEN_WIDTH,
                                         SCREEN_HEIGHT + 200, (0, 0, 0, self.rec_opas_targeted))
            self.win.draw()
            self.score.draw()
            self.score_t.draw()
            self.button.draw()
            self.mainmenuText.draw()

    def generate_score(self):
        text = ""

        text += f"Enemies Kills: {ENEMIES_KILL * 100}\n"

        text += f"Coins: {self.playerObject.coins * 10}\n"

        text += f"Items: {(len(self.playerObject.inventory) + len(self.playerObject.weapons)) * 1000}\n"

        text += f"Hp: {int(self.playerObject.hp * 100)}\n"

        self.total_score = int(self.playerObject.hp * 100 +
                          (len(self.playerObject.inventory) + len(self.playerObject.weapons)) * 1000 +
                          self.playerObject.coins * 10 +
                          ENEMIES_KILL * 100)
        text += f"""TOTAL: {self.total_score}"""

        return arcade.Text(
            text,
            self.playerObject.center_x,
            self.playerObject.center_y - 100,
            (248, 245, 226),
            50,
            font_name="First Time Writing!",
            bold=True,
            multiline=True,
            width=SCREEN_WIDTH / 3,
            align="center",
            anchor_x="center",
            anchor_y="center",
        )

    def save_score(self):
        try:
            with open("SCORES.json", 'r') as file:
                scores = json.load(file)
        except FileNotFoundError:
            with open("SCORES.json", 'w') as file:
                json.dump({}, file)
            with open("SCORES.json", 'r') as file:
                scores = json.load(file)

        try:
            score = scores[f"{self.playerObject.character.name}"]
            if self.total_score > score:
                scores[f"{self.playerObject.character.name}"] = self.total_score
        except KeyError:
            scores[f"{self.playerObject.character.name}"] = self.total_score

        with open("SCORES.json", 'w') as file:
            json.dump(scores, file)


class LoseScreen(arcade.View):
    def __init__(self, gameView):
        super().__init__()
        self.total_score = None
        self.gameView = gameView
        self.playerObject = gameView.playerObject
        self.gamViewScene = gameView.scene

        self.rec_opas = 0
        self.rec_opas_targeted = 150
        self.ifFade = True

        self.Cam = arcade.Camera()
        position = Vec2(
            self.playerObject.center_x - SCREEN_WIDTH / 2,
            self.playerObject.center_y - SCREEN_HEIGHT / 2
        )
        self.Cam.move_to(position)

        self.lose = arcade.Text(
            f"YOU DIED",
            self.playerObject.center_x,
            self.playerObject.center_y + 150,
            (248, 0, 0),
            200,
            font_name="First Time Writing!",
            bold=True,
            anchor_x="center",
            anchor_y="center",
        )

        self.button = WinScreenButton(self.playerObject.center_x, self.lose.bottom - 150)
        self.mainmenuText = arcade.Text(
            f"QUIT",
            self.button.center_x,
            self.button.center_y,
            (248, 245, 226),
            50,
            font_name="First Time Writing!",
            bold=True,
            anchor_x="center",
            anchor_y="center"
        )

        self.gamViewScene.get_sprite_list("Player")[0].turn_left(90)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.button.is_clicked(self.playerObject.center_x - SCREEN_WIDTH / 2 + x, self.playerObject.center_y - SCREEN_HEIGHT / 2 + y):
            self.window.show_view(main.MainMenuView())
            sound.play_random_paper()

    def on_draw(self):
        self.clear()
        self.Cam.use()
        if self.ifFade:
            self.gamViewScene.draw(pixelated=True)
            arcade.draw_rectangle_filled(self.playerObject.center_x, self.playerObject.center_y, SCREEN_WIDTH,
                                         SCREEN_HEIGHT + 200, (0, 0, 0, self.rec_opas))
            self.rec_opas += 1
            if self.rec_opas >= self.rec_opas_targeted:
                self.ifFade = False
                sound.play_sound("sounds/lose.mp3")

        else:
            self.gamViewScene.draw(pixelated=True)
            arcade.draw_rectangle_filled(self.playerObject.center_x, self.playerObject.center_y, SCREEN_WIDTH,
                                         SCREEN_HEIGHT + 200, (0, 0, 0, self.rec_opas_targeted))
            self.lose.draw()
            self.button.draw()
            self.mainmenuText.draw()


def count_kill():
    global ENEMIES_KILL
    ENEMIES_KILL += 1
