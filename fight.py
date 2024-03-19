import arcade

MOUSE_MARGIN = 40
SCREEN_WIDTH = 992
SCREEN_HEIGHT = 572


class Slash(arcade.Sprite):
    def __init__(self, center_x, center_y, scale=1, flip=False):
        self.frames_normal = []
        for i in range(1, 7):
            self.frames_normal.append(arcade.load_texture(f"sprites/player/slash/slash_{i}.png"))
        self.flipped_frames = []
        for i in range(1, 7):
            self.flipped_frames.append(arcade.load_texture(f"sprites/player/slash/slash_{i}.png", flipped_horizontally=True))
        if flip:
            self.frames = self.flipped_frames
        else:
            self.frames = self.frames_normal
        super().__init__(texture=self.frames[0], center_x=center_x, center_y=center_y, scale=scale)
        self.alpha = 150
        self.frames_counter = 1
        self.direction = None
        self.default_cooldown_counter = 0.03
        self._cooldown_counter = self.default_cooldown_counter

    def cooldown(self):
        self._cooldown_counter -= 1/60
        if self._cooldown_counter <= 0:
            if self.frames_counter == len(self.frames) - 1:
                self.kill()
            self._cooldown_counter = self.default_cooldown_counter
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
                if enemyToDamage.direction_move == "Left":
                    slash = Slash(enemyToDamage.center_x, enemyToDamage.center_y, weapon.slash_scale, True)
                else:
                    slash = Slash(enemyToDamage.center_x, enemyToDamage.center_y, weapon.slash_scale)

                gameView.scene.add_sprite("Slash", slash)
                enemyToDamage.damage(weapon.damage * (playerObject.strength / 100))
                weapon.start_cooldown()


def _attack(weapon, enemy):
    pass
