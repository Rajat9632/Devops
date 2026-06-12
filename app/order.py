"""Order module."""
#changedcomment
class Order:
    def __init__(self, order_id: int, item: str):
        self.order_id = order_id
        self.item = item
        self.status = "Pending"

    def complete(self):
        self.status = "Completed"
#changedcomment3
