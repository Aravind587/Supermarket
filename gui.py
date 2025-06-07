import tkinter as tk
from tkinter import ttk, messagebox
import re
try:
    import ttkbootstrap as tbs
    from ttkbootstrap.constants import *
except ImportError:
    import tkinter.ttk as tbs
    from tkinter.constants import *
    print("ttkbootstrap not found. Using default Tkinter styling.")

from data import categories
from cart import CartManager
from payment import PaymentProcessor
from config import USD_TO_INR

class SupermarketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Super Market")
        self.root.geometry("1200x800")

        self.usd_to_inr = USD_TO_INR
        self.cart_manager = CartManager()
        self.payment_processor = PaymentProcessor(self.cart_manager, self.usd_to_inr)
        self.currency_var = tk.StringVar(value="INR")
        self.current_content = None
        self.notebook = None

        self.user_info = {
            "name": "Aravind Kumar Korumilli",
            "email": "aravind.korumilli@gmail.com",
            "address": "123, MG Road, Bangalore, Karnataka, India - 560001",
            "card_details": {
                "card_number": "1234567890123456",
                "expiry": "12/27",
                "cvv": "123",
                "balance": 100000.00
            }
        }

        self.setup_styles()
        self.create_gui()

    def setup_styles(self):
        try:
            self.style = tbs.Style(theme="flatly")
            self.style.configure("TFrame", background="#F5F5DC")
            self.style.configure("TLabel", font=("Arial", 14), background="#e64353")
            self.style.configure("Header", font=("Arial", 14), background="#e61721", foreground="#87d0ed")
            self.style.configure("TButton", font=("Arial", 10))
            self.style.configure("Header.TFrame", background="#17abe6")
            self.style.configure("Header.TLabel", font=("Arial", 35, "bold"), foreground="#1A3C5A")
            self.style.configure("Header.TButton", font=("Arial", 45, "bold"), padding=[8, 4], background="#D4EFDF", foreground="#000000")
            self.style.map("Header.TButton", background=[("active", "#28A745"), ("!active", "#D4EFDF")], foreground=[("active", "#FFFFFF")])
            self.style.configure("WhiteFrame.TFrame", background="#FDF5E6")
            self.style.configure("LightGrayFrame.TFrame", background="#F5F5DC")
            self.style.configure("WhiteCartFrame.TFrame", background="#E6E6FA")
            self.style.configure("OddRowFrame.TFrame", background="#FFE4E1")
            self.style.configure("ItemFrame.TFrame", background="#FDF5E6", relief="solid", borderwidth=1)
            self.style.configure("AddButton.TButton", background="#FF8C00", foreground="#FFFFFF", padding=3, font=("Arial", 14, "bold"))
            self.style.map("AddButton.TButton", background=[("active", "#E07B00")])
            self.style.configure("PaymentForm.TFrame", background="#E6F0FA")
            self.style.configure("PaymentLabel.TLabel", font=("Arial", 12), foreground="#1A3C5A")
            self.style.configure("PaymentButton.TButton", background="#28A745", foreground="#FFFFFF", font=("Arial", 20, "bold"), padding=10)
            self.style.map("PaymentButton.TButton", background=[("active", "#218838")])
            self.style.configure("TNotebook", background="#FDF5E6")
            self.style.configure("TNotebook.Tab", font=("Arial", 12), padding=[10, 5])
            self.style.map("TNotebook.Tab", background=[("active", "#D4EFDF"), ("!active", "#FDF5E6"), ("!active", "!selected", "#FDF5E6", "!disabled", ":hover", "#E0E0E0")])
        except:
            self.style = ttk.Style()
            self.style.configure("TFrame", background="#34c6e0")
            self.style.configure("TLabel", background="#e64353")
            self.style.configure("Header", font=("Arial", 14), background="#e61721", foreground="#87d0ed")
            self.style.configure("Header.TFrame", background="#17abe6")
            self.style.configure("Header.TLabel", font=("Arial", 30, "bold"), background="#34c6e0",  foreground="#1A3C5A")
            self.style.configure("Header.TButton", font=("Arial", 45, "bold"))
            self.style.configure("WhiteFrame.TFrame", background="#FDF5E6")
            self.style.configure("LightGrayFrame.TFrame", background="#F5F5DC")
            self.style.configure("WhiteCartFrame.TFrame", background="#E6E6FA")
            self.style.configure("OddRowFrame.TFrame", background="#FFE4E1")
            self.style.configure("ItemFrame.TFrame", background="#FDF5E6", relief="solid", borderwidth=1)
            self.style.configure("AddButton.TButton", background="#FF8C00", foreground="#FFFFFF")
            self.style.map("AddButton.TButton", background=[("active", "#E07B00")])
            self.style.configure("PaymentForm.TFrame", background="payment.jpg")
            self.style.configure("PaymentLabel.TLabel", font=("Arial", 12), foreground="#1A3C5A")
            self.style.configure("PaymentButton.TButton", background="#28A745", foreground="#FFFFFF", font=("Arial", 20, "bold"))
            self.style.map("PaymentButton.TButton", background=[("active", "#218838")])
            self.style.configure("TNotebook", background="#FDF5E6")
            self.style.configure("TNotebook.Tab", font=("Arial", 12))

    def create_gui(self):
        self.main_frame = ttk.Frame(self.root, style="TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.header_frame = ttk.Frame(self.main_frame, style="Header")
        self.header_frame.pack(fill=tk.X, padx=10, pady=5)

        self.title_label = ttk.Label(self.header_frame, text="Super Market",background="#34c6e0", style="Header.TLabel",font=("arial",30,"bold"),anchor="center")
        self.title_label.pack(side=tk.LEFT, padx=10, expand=True)

        self.account_button = ttk.Button(self.header_frame, text="Account", style="Header.TButton", command=self.show_account_options)
        self.account_button.pack(side=tk.RIGHT, padx=5)

        self.cart_button = ttk.Button(self.header_frame, text="View Cart", style="Header.TButton", command=self.show_cart)
        self.cart_button.pack(side=tk.RIGHT, padx=5)

        self.currency_button = ttk.Button(self.header_frame, textvariable=self.currency_var, style="Header.TButton", command=self.toggle_currency)
        self.currency_button.pack(side=tk.RIGHT, padx=5)

        self.content_frame = ttk.Frame(self.main_frame, style="WhiteFrame.TFrame")
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.show_products()

    def clear_content(self):
        if self.current_content:
            self.current_content.destroy()
        self.current_content = None

    def show_products(self):
        self.clear_content()
        self.notebook = ttk.Notebook(self.content_frame, style="TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.current_content = self.notebook

        for category in categories:
            tab = ttk.Frame(self.notebook, style="WhiteFrame.TFrame")
            self.notebook.add(tab, text=category["name"])
            self.create_product_tab(tab, category["items"])

    def create_product_tab(self, tab, items):
        canvas = tk.Canvas(tab, bg="#FDF5E6", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style="WhiteFrame.TFrame")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        self.update_products(scrollable_frame, items)

    def update_products(self, parent, items):
        for widget in parent.winfo_children():
            widget.destroy()

        row = 0
        col = 0
        max_width = self.root.winfo_screenwidth() - 50
        item_width = 220
        items_per_row = max(1, max_width // item_width)

        for idx, item in enumerate(items):
            if col >= items_per_row:
                col = 0
                row += 1

            item_frame = ttk.Frame(parent, style="TLabel", padding=10, width=240, height=240)
            item_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            item_frame.grid_propagate(False)
            item_frame.grid_columnconfigure(0, weight=1)
            item_frame.grid_rowconfigure([0, 1, 2, 3, 4], weight=1, uniform="row")

            name_label = ttk.Label(item_frame, text=item["name"], font=("Arial", 12, "bold"), style="TLabel",foreground="#87d0ed", wraplength=180, anchor="center")
            name_label.grid(row=0, column=0, sticky="ew")

            desc_label = ttk.Label(item_frame, text=item["description"], font=("Arial", 9,"bold"), style="TLabel",foreground="#87d0ed", wraplength=200, anchor="center")
            desc_label.grid(row=1, column=0, sticky="ew")

            price = item["price"] / self.usd_to_inr if self.currency_var.get() == "USD" else item["price"]
            currency_symbol = "$" if self.currency_var.get() == "USD" else "₹"
            price_label = ttk.Label(item_frame, text=f"price:{currency_symbol}{price:.2f}/{item['unit']}", font=("Arial", 15), style="TLabel",anchor="center",foreground="#b9f52c")
            price_label.grid(row=2, column=0, sticky="ew")

            quantity_var = tk.StringVar(value="1")
            quantity_entry = ttk.Entry(item_frame, textvariable=quantity_var, width=5, justify="center")
            quantity_entry.grid(row=3, column=0, sticky="ew", padx=5)

            add_button = ttk.Button(item_frame, text="Add to Cart", style="AddButton.TButton", command=lambda i=item, q=quantity_var: self.add_to_cart(i, q))
            add_button.grid(row=4, column=0, sticky="ew", padx=5)

            col += 1

    def add_to_cart(self, item, quantity_var):
        try:
            quantity = float(quantity_var.get())
            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be greater than zero.")
                return
            self.cart_manager.add_to_cart(item, quantity)
            messagebox.showinfo("Success", f"{item['name']} x{quantity} added to cart.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid quantity.")

    def toggle_currency(self):
        current = self.currency_var.get()
        self.currency_var.set("USD" if current == "INR" else "INR")
        self.refresh_content()

    def refresh_content(self):
        if self.notebook:
            selected_tab = self.notebook.index(self.notebook.select())
            self.show_products()
            self.notebook.select(selected_tab)
        elif "cart" in str(self.current_content):
            self.show_cart()
        elif "payment" in str(self.current_content):
            self.show_payment_form()
        elif "orders" in str(self.current_content):
            self.show_orders()
        elif "profile" in str(self.current_content):
            self.show_profile()

    def show_cart(self):
        self.clear_content()
        cart_frame = ttk.Frame(self.content_frame, style="WhiteCartFrame.TFrame")
        cart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.current_content = cart_frame

        total = 0
        for idx, cart_item in enumerate(self.cart_manager.cart):
            item = cart_item["item"]
            quantity = cart_item["quantity"]
            price = item["price"] / self.usd_to_inr if self.currency_var.get() == "USD" else item["price"]
            currency_symbol = "$" if self.currency_var.get() == "USD" else "₹"
            subtotal = price * quantity
            total += subtotal

            row_frame = ttk.Frame(cart_frame, style="TLabel")
            row_frame.pack(fill=tk.X, padx=5, pady=5)

            ttk.Label(row_frame, text=item["name"], style="TLabel", width=30).pack(side=tk.LEFT, padx=10, pady=10)
            ttk.Label(row_frame, text=f"x{quantity}{item['unit']}", style="TLabel", width=10).pack(side=tk.LEFT, padx=5, pady=10)
            ttk.Label(row_frame, text=f"{currency_symbol}{subtotal:.2f}", style="TLabel", width=15).pack(side=tk.LEFT, padx=5, pady=10)
            ttk.Button(row_frame, text="Remove", style="AddButton.TButton", command=lambda i=idx: self.remove_from_cart(i)).pack(side=tk.RIGHT, padx=5, pady=10)

        currency_symbol = "$" if self.currency_var.get() == "USD" else "₹"
        ttk.Label(cart_frame, text=f"Total: {currency_symbol}{total:.2f}", font=("Arial", 14, "bold"), background="#34c6e0").pack(pady=10)
        ttk.Button(cart_frame, text="Proceed to Checkout", style="PaymentButton.TButton", command=self.show_payment_form).pack(pady=5)
        ttk.Button(cart_frame, text="Back to Products", style="PaymentButton.TButton", command=self.show_products).pack(pady=5)

    def remove_from_cart(self, index):
        self.cart_manager.remove_from_cart(index)
        self.show_cart()

    def show_payment_form(self):
        if not self.cart_manager.cart:
            messagebox.showerror("Error", "Your cart is empty.")
            return

        self.clear_content()
        payment_frame = ttk.Frame(self.content_frame, style="PaymentForm.TFrame", padding=20)
        payment_frame.pack(fill=tk.BOTH, expand=True)
        self.current_content = payment_frame

        ttk.Label(payment_frame, text="Payment Details", font=("Arial", 16, "bold"),background="#34c6e0", style="PaymentLabel.TLabel").pack(pady=10)

        total = sum(item["item"]["price"] * item["quantity"] for item in self.cart_manager.cart)
        if self.currency_var.get() == "USD":
            total /= self.usd_to_inr
        currency_symbol = "$" if self.currency_var.get() == "USD" else "₹"
        ttk.Label(payment_frame, text=f"Total Amount: {currency_symbol}{total:.2f}",background="#34c6e0", style="PaymentLabel.TLabel").pack(pady=5)

        ttk.Label(payment_frame, text="Card Number:",background="#34c6e0", style="PaymentLabel.TLabel").pack()
        card_number = ttk.Entry(payment_frame, width=30)
        card_number.pack(pady=5)
        card_number.insert(0, self.user_info["card_details"]["card_number"])

        ttk.Label(payment_frame, text="Expiry (MM/YY):",background="#34c6e0", style="PaymentLabel.TLabel").pack()
        expiry = ttk.Entry(payment_frame, width=10)
        expiry.pack(pady=5)
        expiry.insert(0, self.user_info["card_details"]["expiry"])

        ttk.Label(payment_frame, text="CVV:",background="#34c6e0", style="PaymentLabel.TLabel").pack()
        cvv = ttk.Entry(payment_frame, width=5)
        cvv.pack(pady=5)
        cvv.insert(0, self.user_info["card_details"]["cvv"])

        button_frame = ttk.Frame(payment_frame, style="PaymentForm.TFrame")
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="Pay Now", style="PaymentButton.TButton", command=lambda: self.payment_processor.process_payment(
            card_number.get(), expiry.get(), cvv.get(), total, self.user_info, self.currency_var.get(), self.show_products)).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Pay for Delivery", style="PaymentButton.TButton", command=lambda: self.payment_processor.process_pay_for_delivery(
            card_number.get(), expiry.get(), cvv.get(), total, self.user_info, self.currency_var.get(), self.show_products)).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Pay on Delivery", style="PaymentButton.TButton", command=lambda: self.payment_processor.process_pay_on_delivery(
            total, self.user_info, self.currency_var.get(), self.show_products)).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Back to Products", style="PaymentButton.TButton", command=self.show_products).pack(pady=5)

    def show_account_options(self):
        self.clear_content()
        account_frame = ttk.Frame(self.content_frame, style="WhiteFrame.TFrame")
        account_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.current_content = account_frame

        ttk.Button(account_frame, text="View Profile", style="PaymentButton.TButton", command=self.show_profile).pack(pady=5)
        ttk.Button(account_frame, text="View Orders", style="PaymentButton.TButton", command=self.show_orders).pack(pady=5)
        ttk.Button(account_frame, text="Back to Products", style="PaymentButton.TButton", command=self.show_products).pack(pady=5)

    def show_profile(self):
        self.clear_content()
        profile_frame = ttk.Frame(self.content_frame, style="PaymentForm.TFrame", padding=20)
        profile_frame.pack(fill=tk.BOTH, expand=True)
        self.current_content = profile_frame

        ttk.Label(profile_frame, text="User Profile", font=("Arial", 16, "bold"), style="PaymentLabel.TLabel").pack(pady=10)

        ttk.Label(profile_frame, text=f"Name: {self.user_info['name']}", style="PaymentLabel.TLabel").pack(pady=5)
        ttk.Label(profile_frame, text=f"Email: {self.user_info['email']}", style="PaymentLabel.TLabel").pack(pady=5)
        ttk.Label(profile_frame, text=f"Address: {self.user_info['address']}", style="PaymentLabel.TLabel").pack(pady=5)
        balance = self.user_info["card_details"]["balance"] / self.usd_to_inr if self.currency_var.get() == "USD" else self.user_info["card_details"]["balance"]
        currency_symbol = "$" if self.currency_var.get() == "USD" else "₹"
        ttk.Label(profile_frame, text=f"Balance: {currency_symbol}{balance:.2f}", style="PaymentLabel.TLabel").pack(pady=5)

        ttk.Button(profile_frame, text="Back", style="PaymentButton.TButton", command=self.show_account_options).pack(pady=10)

    def show_orders(self):
        self.clear_content()
        orders_frame = ttk.Frame(self.content_frame, style="TLabel")
        orders_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.current_content = orders_frame

        ttk.Label(orders_frame, text="My Orders", font=("Arial", 16, "bold"), style="TLabel").pack(pady=10)

        for idx, order in enumerate(self.cart_manager.orders):
            order_frame = ttk.Frame(orders_frame, style="OddRowFrame.TFrame" if idx % 2 else "WhiteCartFrame.TFrame")
            order_frame.pack(fill=tk.X, padx=5, pady=2)

            total = order["total"] / self.usd_to_inr if self.currency_var.get() == "USD" else order["total"]
            currency_symbol = "$" if self.currency_var.get() == "USD" else "₹"
            items_summary = ", ".join(f"\n{item['item']['name']} x{item['quantity']}" for item in order["items"])
            payment_status = order.get("payment_status", "Not Done")
            ttk.Label(order_frame, text=f"Order {idx + 1}: {items_summary}", style="TLabel", wraplength=600).pack(side=tk.LEFT, padx=10, pady=10)
            ttk.Label(order_frame, text=f"Total: {currency_symbol}{total:.2f}", style="TLabel").pack(side=tk.LEFT, padx=5, pady=10)
            ttk.Label(order_frame, text=f"Payment Status: {payment_status}", style="TLabel").pack(side=tk.LEFT, padx=5, pady=10)
            ttk.Label(order_frame, text=f"Delivery: {order['delivery_date']}", style="TLabel").pack(side=tk.LEFT, padx=5, pady=10)
            if payment_status == "Not Done":
                ttk.Button(order_frame, text="Complete Payment", style="PaymentButton.TButton", 
                           command=lambda i=idx: self.payment_processor.complete_delivery_payment(
                               i, self.user_info, self.currency_var.get(), self.show_orders)).pack(side=tk.RIGHT, padx=5, pady=10)

        ttk.Button(orders_frame, text="Back", style="PaymentButton.TButton", command=self.show_account_options).pack(pady=10)