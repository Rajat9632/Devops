"""Inventory module."""
#ESHWAR
#changed comment2
class Inventory:
    def __init__(self):
        self.items = {}

    def add_item(self, item_name: str, quantity: int):
        if item_name in self.items:
            self.items[item_name] += quantity
        else:
            self.items[item_name] = quantity

    def get_stock(self, item_name: str) -> int:
        return self.items.get(item_name, 0)
