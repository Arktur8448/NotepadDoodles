import arcade
import math
import items


class Bullet(arcade.Sprite):
    def __init__(self, sprite, bullet_speed, damage, distance, startPos):
        super().__init__(filename=sprite, scale=0.5)
        self.position = startPos
        self.start_pos = self.position
        self.change_x = bullet_speed * 10
        self.change_y = bullet_speed * 10
        self.distance = distance
        self.bullet_speed = bullet_speed
        self.damage = damage

    def move(self, scene, delta_time: float = 1 / 60):
        self.position = (
            self.center_x + self.change_x * delta_time,
            self.center_y + self.change_y * delta_time,
        )
        if arcade.get_distance(self.center_x, self.center_y, self.start_pos[0], self.start_pos[1]) > self.distance:
            self.kill()
        for e in arcade.check_for_collision_with_list(self, scene.get_sprite_list("Enemies")):
            e.damage(self.damage)
            self.kill()

    def shoot(self, pos):
        x, y = pos
        diff_x = x - self.center_x
        diff_y = y - self.center_y
        angle = math.atan2(diff_y, diff_x)
        angle_deg = math.degrees(angle)
        if angle_deg < 0:
            angle_deg += 360
        self.angle = angle_deg

        self.change_x = math.cos(angle) * self.bullet_speed
        self.change_y = math.sin(angle) * self.bullet_speed


class Slash(arcade.Sprite):
    def __init__(self, center_x, center_y, scale=1, flip=False):
        self.frames_normal = []
        for i in range(1, 7):
            self.frames_normal.append(arcade.load_texture(f"sprites/player/slash/slash_{i}.png"))
        self.flipped_frames = []
        for i in range(1, 7):
            self.flipped_frames.append(
                arcade.load_texture(f"sprites/player/slash/slash_{i}.png", flipped_horizontally=True))
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
        self._cooldown_counter -= 1 / 60
        if self._cooldown_counter <= 0:
            if self.frames_counter == len(self.frames) - 1:
                self.kill()
            self._cooldown_counter = self.default_cooldown_counter
            self.texture = self.frames[self.frames_counter]
            self.frames_counter += 1


def update(gameView):
    playerObject = gameView.playerObject
    weapons = playerObject.weapons
    scene = gameView.scene
    enemies = gameView.scene.get_sprite_list("Enemies")
    slashes = gameView.scene.get_sprite_list("Slash")
    bullets = gameView.scene.get_sprite_list("Bullets")

    for s in slashes:
        s.cooldown()

    for weapon in weapons:
        if type(weapon) is items.Weapon:
            weapon.cooldown()
            if weapon.canAttack:
                enemyToDamage = None
                for e in enemies:
                    try:
                        if e.distance < weapon.attack_range:
                            if enemyToDamage is None:
                                enemyToDamage = e
                            elif e.distance < enemyToDamage.distance:
                                enemyToDamage = e
                    except:
                        continue
                if enemyToDamage is not None:
                    if enemyToDamage.direction_move == "Left":
                        slash = Slash(enemyToDamage.center_x, enemyToDamage.center_y, weapon.slash_scale, True)
                    else:
                        slash = Slash(enemyToDamage.center_x, enemyToDamage.center_y, weapon.slash_scale)

                    gameView.scene.add_sprite("Slash", slash)
                    enemyToDamage.damage(weapon.damage * (playerObject.strength / 100))
                    weapon.start_cooldown()
        if type(weapon) is items.RangedWeapon or type(weapon) is items.Wand:
            weapon.cooldown()
            if weapon.canAttack:
                enemyToDamage = None
                for e in enemies:
                    try:
                        if e.distance < weapon.attack_range:
                            if enemyToDamage is None:
                                enemyToDamage = e
                            elif e.distance < enemyToDamage.distance:
                                enemyToDamage = e
                    except:
                        continue
                if enemyToDamage is not None:
                    damage_multiplayer = 1
                    if type(weapon) is items.RangedWeapon:
                        damage_multiplayer = (playerObject.accuracy / 100)
                    elif type(weapon) is items.Wand:
                        damage_multiplayer = (playerObject.agility / 100)

                    b = Bullet(weapon.bullet_path, weapon.bullet_speed, weapon.damage * damage_multiplayer, weapon.attack_range, playerObject.position)
                    b.shoot(enemyToDamage.position)
                    scene.add_sprite("Bullets", b)
                    weapon.start_cooldown()
