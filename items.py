import arcade


class Item(arcade.Sprite):
    def __init__(self, sprite_path, description, item_rarity, name, price_buy, price_sell):
        super().__init__(filename=sprite_path, scale=1)
        self.description = description
        self.item_rarity = item_rarity
        self.name = name
        self.price_buy = price_buy
        self.price_sell = price_sell


