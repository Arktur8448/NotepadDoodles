import arcade

MOUSE_MARGIN = 40
SCREEN_WIDTH = 992
SCREEN_HEIGHT = 572


class Slash(arcade.Sprite):
    def __init__(self, center_x, center_y):
        self.frames = [arcade.Texture.create_filled("col", (50, 30), (0, 0, 0, 200)),
                       arcade.Texture.create_filled("col", (50, 30), (0, 0, 0, 100)),
                       arcade.Texture.create_filled("col", (50, 30), (0, 0, 0, 200))]

        super().__init__(texture=self.frames[0], center_x=center_x, center_y=center_y)
        self.frames_counter = 1
        self.direction = None
        self.cooldown_counter = 0.3

    def cooldown(self):
        self.cooldown_counter -= 1/60
        if self.cooldown_counter <= 0:
            if self.frames_counter == len(self.frames) - 1:
                self.kill()
            self.texture = self.frames[self.frames_counter]
            self.frames_counter += 1


def update(gameView):
    playerObject = gameView.playerObject
    weapons = playerObject.weapons
    enemies = gameView.scene.get_sprite_list("Enemies")
    slashes = gameView.scene.get_sprite_list("Slash")

    for s in slashes:
        s.cooldown()

    for weapon in weapons:
        weapon.cooldown()
        if weapon.canAttack:
            texture = arcade.Texture.create_filled("col", (weapon.attack_range, weapon.attack_range), (0, 0, 0, 100))
            sprite = arcade.Sprite(texture=texture, center_x=playerObject.center_x, center_y=playerObject.center_y)
            sprite.draw()
            enemiesInCollision = sprite.collides_with_list(enemies)
            enemyToDamage = None
            for e in enemiesInCollision:
                if enemyToDamage is None:
                    enemyToDamage = e
                elif e.distance < enemyToDamage.distance:
                    enemyToDamage = e
            if enemyToDamage is not None:
                gameView.scene.add_sprite("Slash", Slash(enemyToDamage.center_x,enemyToDamage.center_y))
                enemyToDamage.damage(weapon.damage)
                weapon.start_cooldown()


def _attack(weapon, enemy):
    pass
