import arcade
import time
import math

MOUSE_MARGIN = 40
SCREEN_WIDTH = 992
SCREEN_HEIGHT = 572


class Slash(arcade.Sprite):
    def __init__(self,center_x, center_y, image_width=55, image_height=65, scale=1):
        super().__init__(filename="sprites/player/slash.png",
                         center_x=center_x, center_y=center_y,
                         image_width=image_width, image_height=image_height, scale=scale)
        self.direction = None


def get_slash(player_object, scene, x, y, slash_damage, slash_stamina, slash_cooldown, slash_duration):
    if len(scene.get_sprite_list("Slash")) == 0 and player_object.stamina > slash_stamina and player_object.slash_cooldown_time <= 0:
        player_object.stamina -= slash_stamina
        slash = Slash(center_x=player_object.center_x, center_y=player_object.center_y)
        x -= SCREEN_WIDTH / 2
        y -= SCREEN_HEIGHT / 2
        if -MOUSE_MARGIN < x < MOUSE_MARGIN:
            if y > 0:
                slash.direction = "Up"
                slash.center_x += 0
                slash.center_y += 60
            else:
                slash.direction = "Down"
                slash.center_x += 0
                slash.center_y += -55
        elif -MOUSE_MARGIN < y < MOUSE_MARGIN:
            if x > 0:
                slash.direction = "Right"
                slash.center_x += 50
                slash.center_y += 0
            else:
                slash.direction = "Left"
                slash.center_x += -50
                slash.center_y += 0
        else:
            if x > MOUSE_MARGIN and y > MOUSE_MARGIN:
                slash.direction = "UpRight"
                slash.center_x += 25
                slash.center_y += 50
            elif x < MOUSE_MARGIN < y:
                slash.direction = "UpLeft"
                slash.center_x += -25
                slash.center_y += 50
            elif x > MOUSE_MARGIN > y:
                slash.direction = "DownRight"
                slash.center_x += 25
                slash.center_y += -50
            elif x < MOUSE_MARGIN and y < MOUSE_MARGIN:
                slash.direction = "DownLeft"
                slash.center_x += -25
                slash.center_y += -50
        radian = math.atan2(x, y)
        degree = math.degrees(radian)
        slash.turn_right(degree)

        scene.add_sprite("Slash", slash)
        for e in scene.get_sprite_list("NPC"):
            if arcade.check_for_collision(e, slash):
                e.health -= slash_damage
                if e.health <= 0:
                    e.kill()

        player_object.last_time_slash = time.perf_counter() + slash_duration
        player_object.slash_cooldown_time = slash_cooldown


def update(player_object, physics_engine, scene):
    if player_object.slash_cooldown_time > 0:
        player_object.slash_cooldown_time -= 1/60
    if len(scene.get_sprite_list("Slash")) > 0:
        if time.perf_counter() > player_object.last_time_slash:
            for s in scene.get_sprite_list("Slash"):
                s.kill()
                player_object.can_move = True
                player_object.ifAttack = False
        else:
            for slash in scene.get_sprite_list("Slash"):
                player_object.can_move = False
                player_object.ifAttack = True
                player_object.direction_attack = slash.direction
                slash.center_x = player_object.center_x
                slash.center_y = player_object.center_y
                attack_force = (0, 0)
                attack_force_power = 3000
                match slash.direction:
                    case "Down":
                        slash.center_x += 0
                        slash.center_y += -55
                        attack_force = (0, -attack_force_power)
                    case "DownLeft":
                        slash.center_x += -25
                        slash.center_y += -50
                        attack_force = (-attack_force_power, -attack_force_power)
                    case "Left":
                        slash.center_x += -50
                        slash.center_y += 0
                        attack_force = (-attack_force_power, 0)
                    case "UpLeft":
                        slash.center_x += -25
                        slash.center_y += 50
                        attack_force = (-attack_force_power, attack_force_power)
                    case "Up":
                        slash.center_x += 0
                        slash.center_y += 60
                        attack_force = (0, attack_force_power)
                    case "UpRight":
                        slash.center_x += 25
                        slash.center_y += 50
                        attack_force = (attack_force_power, attack_force_power)
                    case "Right":
                        slash.center_x += 50
                        slash.center_y += 0
                        attack_force = (attack_force_power, 0)
                    case "DownRight":
                        slash.center_x += 25
                        slash.center_y += -50
                        attack_force = (attack_force_power, -attack_force_power)
                physics_engine.apply_force(player_object, attack_force)
