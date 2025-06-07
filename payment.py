import re
from tkinter import messagebox
from email_service import send_order_confirmation_email, send_payment_completion_email

class PaymentProcessor:
    def __init__(self, cart_manager, usd_to_inr):
        self.cart_manager = cart_manager
        self.usd_to_inr = usd_to_inr

    def process_payment(self, card_number, expiry, cvv, total, user_info, currency, callback):
        """
        Process a card payment and send an order confirmation email.
        
        Args:
            card_number (str): 16-digit card number.
            expiry (str): Expiry date in MM/YY format.
            cvv (str): 3-digit CVV code.
            total (float): Total amount to charge.
            user_info (dict): User information including card details and email.
            currency (str): Currency used ('INR' or 'USD').
            callback (function): Callback function to execute after successful payment.
        """
        if not re.match(r"^\d{16}$", card_number):
            messagebox.showerror("Error", "Invalid card number. Must be 16 digits.")
            return
        if not re.match(r"^(0[1-9]|1[0-2])\/\d{2}$", expiry):
            messagebox.showerror("Error", "Invalid expiry date. Use MM/YY format.")
            return
        if not re.match(r"^\d{3}$", cvv):
            messagebox.showerror("Error", "Invalid CVV. Must be 3 digits.")
            return

        if currency == "USD":
            total *= self.usd_to_inr

        if user_info["card_details"]["balance"] < total:
            messagebox.showerror("Error", f"Insufficient funds. Your balance is ₹{user_info['card_details']['balance']:.2f}, but the cart total is ₹{total:.2f}.")
            return

        user_info["card_details"]["balance"] -= total
        order = self.cart_manager.place_order()
        order["payment_status"] = "Done"
        send_order_confirmation_email(order, user_info, currency, self.usd_to_inr, len(self.cart_manager.orders))
        messagebox.showinfo("Success", "Payment successful! Order placed. Confirmation email sent.")
        self.cart_manager.cart = []
        callback()

    def process_pay_for_delivery(self, card_number, expiry, cvv, total, user_info, currency, callback):
        """
        Process a pay-for-delivery payment and send an order confirmation email.
        
        Args:
            card_number (str): 16-digit card number.
            expiry (str): Expiry date in MM/YY format.
            cvv (str): 3-digit CVV code.
            total (float): Total amount to charge.
            user_info (dict): User information including card details and email.
            currency (str): Currency used ('INR' or 'USD').
            callback (function): Callback function to execute after successful payment.
        """
        if not re.match(r"^\d{16}$", card_number):
            messagebox.showerror("Error", "Invalid card number. Must be 16 digits.")
            return
        if not re.match(r"^(0[1-9]|1[0-2])\/\d{2}$", expiry):
            messagebox.showerror("Error", "Invalid expiry date. Use MM/YY format.")
            return
        if not re.match(r"^\d{3}$", cvv):
            messagebox.showerror("Error", "Invalid CVV. Must be 3 digits.")
            return

        if currency == "USD":
            total *= self.usd_to_inr

        if user_info["card_details"]["balance"] < total:
            messagebox.showerror("Error", f"Insufficient funds. Your balance is ₹{user_info['card_details']['balance']:.2f}, but the cart total is ₹{total:.2f}.")
            return

        user_info["card_details"]["balance"] -= total
        order = self.cart_manager.place_order()
        order["payment_status"] = "Done"
        send_order_confirmation_email(order, user_info, currency, self.usd_to_inr, len(self.cart_manager.orders))
        messagebox.showinfo("Success", "Payment successful! Order placed for delivery. Confirmation email sent.")
        self.cart_manager.cart = []
        callback()

    def process_pay_on_delivery(self, total, user_info, currency, callback):
        """
        Process a pay-on-delivery order and send a confirmation email.
        
        Args:
            total (float): Total amount of the order.
            user_info (dict): User information including email.
            currency (str): Currency used ('INR' or 'USD').
            callback (function): Callback function to execute after order placement.
        """
        if currency == "USD":
            total *= self.usd_to_inr
        order = self.cart_manager.place_order()
        order["payment_status"] = "Not Done"
        send_order_confirmation_email(order, user_info, currency, self.usd_to_inr, len(self.cart_manager.orders))
        messagebox.showinfo("Success", "Order placed! Payment will be collected on delivery. Confirmation email sent.")
        self.cart_manager.cart = []
        callback()

    def complete_delivery_payment(self, order_index, user_info, currency, callback):
        """
        Complete payment for a pay-on-delivery order and update status.
        
        Args:
            order_index (int): Index of the order in cart_manager.orders.
            user_info (dict): User information including card details and email.
            currency (str): Currency used ('INR' or 'USD').
            callback (function): Callback function to refresh the orders view.
        """
        if not (0 <= order_index < len(self.cart_manager.orders)):
            messagebox.showerror("Error", "Invalid order selected.")
            return

        order = self.cart_manager.orders[order_index]
        if order.get("payment_status") != "Not Done":
            messagebox.showerror("Error", "Payment already completed for this order.")
            return

        total = order["total"]
        if currency == "USD":
            total *= self.usd_to_inr


        if user_info["card_details"]["balance"] < total:
            messagebox.showerror("Error", f"Insufficient funds. Your balance is ₹{user_info['card_details']['balance']:.2f}, but the order total is ₹{total:.2f}.")
            return

        # Deduct the amount from balance
        user_info["card_details"]["balance"] -= total
        # Update payment status
        order["payment_status"] = "Done"
        # Send payment completion email
        send_payment_completion_email(order, user_info, currency, self.usd_to_inr, order_index + 1)
        messagebox.showinfo("Success", "Payment completed! Confirmation email sent.")
        callback()