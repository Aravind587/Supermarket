from datetime import datetime, timedelta

class CartManager:
    def __init__(self):
        self.cart = []
        self.orders = []

    def add_to_cart(self, item, quantity):
        """
        Add an item to the cart with the specified quantity.
        
        Args:
            item (dict): Item details including id, name, price, etc.
            quantity (float): Quantity of the item to add.
        """
        self.cart.append({"item": item, "quantity": quantity})

    def remove_from_cart(self, index):
        """
        Remove an item from the cart by index.
        
        Args:
            index (int): Index of the item to remove.
        """
        if 0 <= index < len(self.cart):
            self.cart.pop(index)

    def place_order(self):
        """
        Place an order from the current cart and clear the cart.
        
        Returns:
            dict: Order details including items, total, and delivery date.
        """
        if not self.cart:
            return None

        total = sum(item["item"]["price"] * item["quantity"] for item in self.cart)
        delivery_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
        order = {
            "items": self.cart.copy(),
            "total": total,
            "delivery_date": delivery_date
        }
        self.orders.append(order)
        self.cart = []
        return order