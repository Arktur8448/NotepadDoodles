import random

import arcade


class Coin(arcade.Sprite):
    def __init__(self, value, x, y):
        scale = 0.5
        if value > 5:
            scale = 0.6
        if value > 10:
            scale = 0.7
        if value > 20:
            scale = 0.8
        if value > 50:
            scale = 1
        super().__init__(filename="sprites/coin.png", scale=scale, center_x=x + random.randint(0, 50), center_y=y + random.randint(0, 50))
        self.distance = 99999999999999999
        self.move_speed = 5
        self._move_force = (0, 0)
        self.value = value

    def move(self, playerObject):
        if self.distance < 50:
            self.collect(playerObject)
        self.distance = ((playerObject.center_x - self.center_x) ** 2 + (
                playerObject.center_y - self.center_y) ** 2) ** 0.5
        if self.distance < 400:
            if self.center_y < playerObject.center_y:
                self.center_y += min(self.move_speed, playerObject.center_y - self.center_y)

            elif self.center_y > playerObject.center_y:
                self.center_y -= min(self.move_speed, self.center_y - playerObject.center_y)

            if self.center_x < playerObject.center_x:
                self.center_x += min(self.move_speed, playerObject.center_x - self.center_x)
            elif self.center_x > playerObject.center_x:
                self.center_x -= min(self.move_speed, self.center_x - playerObject.center_x)

    def collect(self, playerObject):
        playerObject.coins += self.value
        self.kill()
