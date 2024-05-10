import items
import random

weapons = [
    items.Weapon("sprites/items/weapons/dagger.png", "Dagger", damage=7, speed=0.5, attack_range=0.75, price_buy=150),
    items.Weapon("sprites/coin.png", "Axe", damage=15, speed=1.5, attack_range=1, slash_scale=1.5, price_buy=250),
    items.Weapon("sprites/items/weapons/sword.png", "Sword", damage=10, price_buy=100),
    items.Weapon("sprites/items/weapons/greatSword.png", "Great Sword", damage=20, speed=2, attack_range=2, slash_scale=2, price_buy=250)
]

ranged = [
    items.RangedWeapon("sprites/coin.png", "sprites/items/weapons/bullets/arrow.png", "Bow", damage=5, speed=1.5, attack_range=2, price_buy=150),
]

wands = [
    items.Wand("sprites/coin.png", "sprites/items/weapons/bullets/magic_bullet.png", "Wand", damage=5, speed=1, attack_range=2, price_buy=150),
]


def random_weapon():
    return random.choice(weapons)


def random_ranged():
    return random.choice(ranged)


def random_wand():
    return random.choice(wands)
