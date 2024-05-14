import items
import random

weapons = [
    items.Weapon("sprites/items/weapons/dagger.png", "Dagger", damage=7, speed=0.5, attack_range=0.75, price_buy=150),
    items.Weapon("sprites/items/weapons/axe.png", "Axe", damage=15, speed=1.5, attack_range=1.25, slash_scale=1.5, price_buy=200),
    items.Weapon("sprites/items/weapons/sword.png", "Sword", damage=10, price_buy=100),
    items.Weapon("sprites/items/weapons/greatSword.png", "Great Sword", damage=20, speed=2, attack_range=1.5, slash_scale=2, price_buy=250)
]

ranged = [
    items.RangedWeapon("sprites/items/weapons/bows/bow.png", "sprites/items/weapons/bullets/arrow.png", "Bow", damage=5, speed=1.5, attack_range=2, price_buy=150),
    items.RangedWeapon("sprites/items/weapons/bows/fast_bow.png", "sprites/items/weapons/bullets/arrow.png", "Fast Bow", damage=3, speed=0.5, attack_range=2.5, price_buy=250, bullet_speed=1.5),
    items.RangedWeapon("sprites/items/weapons/bows/hunter_bow.png", "sprites/items/weapons/bullets/arrow.png", "Hunter Bow", damage=10, speed=2, attack_range=3, price_buy=250, bullet_speed=0.8),
]

wands = [
    items.Wand("sprites/items/weapons/wands/wand.png", "sprites/items/weapons/bullets/magic_bullet.png", "Wand", damage=5, speed=1, attack_range=2, price_buy=150),
    items.Wand("sprites/items/weapons/wands/strong_wand.png", "sprites/items/weapons/bullets/magic_bullet.png", "Strong Wand", damage=15, speed=1.75, attack_range=1.75, price_buy=250),
    items.Wand("sprites/items/weapons/wands/fast_wand.png", "sprites/items/weapons/bullets/magic_bullet.png", "Fast Wand", damage=3, speed=0.5, attack_range=2.5, price_buy=250),
]

rings = [
    items.Ring("sprites/items/rings/ring_heart.png", "Ring of HP", 100, "max_hp", "HP"),
    items.Ring("sprites/items/rings/ring_heart.png", "Ring of HP Regen Rate", 100, "hp_regen_rate", "HP Regen Rate"),
    items.Ring("sprites/items/rings/ring_light.png", "Ring of Stamina", 100, "max_stamina", "Stamina"),
    items.Ring("sprites/items/rings/ring_light.png", "Ring of Stamina Regen Rate", 100, "stamina_regen_rate", "Stamina Regen Rate"),
    items.Ring("sprites/items/rings/ring_strenght.png", "Ring of Strength", 100, "strength"),
    items.Ring("sprites/items/rings/ring_agility.png", "Ring of Agility", 100, "agility"),
    items.Ring("sprites/items/rings/ring_accuracy.png", "Ring of Accuracy", 100, "accuracy"),
    items.Ring("sprites/items/rings/ring_move.png", "Ring of Movement Speed", 100, "movement_speed", "Movement Speed"),
    items.Ring("sprites/items/rings/ring_move.png", "Ring of Dash Distance", 100, "dash_distance", "Dash Distance"),
    items.Ring("sprites/items/rings/ring_move.png", "Ring of Dash Cooldown", 100, "dash_cooldown", "Dash Cooldown", percentage_range=(-30, -10)),
]


def random_weapon():
    return random.choice(weapons)


def random_ranged():
    return random.choice(ranged)


def random_wand():
    return random.choice(wands)


def random_ring():
    r = random.choice(rings)
    r.regenerate()
    return r


def random_tool():
    a = random.randint(1,4)
    if a == 1:
        return random_weapon()
    elif a == 2:
        return random_ranged()
    elif a == 3:
        return random_wand()
    elif a == 4:
        return random_ring()


def random_util():
    a = random.randint(1, 2)
    if a == 1:
        return random_ring()
    elif a == 2:
        return items.Potion("sprites/items/potion.png", "Potion of HP", 150, random.randint(20, 50))


def random_item():
    a = random.randint(1, 2)
    if a == 1:
        return random_tool()
    elif a == 2:
        return random_util()
