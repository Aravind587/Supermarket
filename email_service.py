import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD

def send_order_confirmation_email(order, user_info, currency, usd_to_inr, order_number):
    """
    Send an order confirmation email to the user.
    
    Args:
        order (dict): Order details containing items, total, delivery date, and payment status.
        user_info (dict): User information including name, email, and address.
        currency (str): Currency used ('INR' or 'USD').
        usd_to_inr (float): Conversion rate from USD to INR.
        order_number (int): Unique order number.
    """
    try:
        # Prepare email content
        subject = f"Order Confirmation - Order #{order_number}"
        sender = SMTP_USER
        recipient = user_info["email"]
        
        # Create MIME message
        msg = MIMEMultipart()
        msg["From"] = f"Super-Market <{sender}>"
        msg["To"] = recipient
        msg["Subject"] = subject

        # Format order details
        currency_symbol = "$" if currency == "USD" else "₹"
        total = order["total"] / usd_to_inr if currency == "USD" else order["total"]
        items_summary = "\n".join(
            f"{item['item']['name']} x{item['quantity']} - {currency_symbol}{(item['item']['price'] / usd_to_inr if currency == 'USD' else item['item']['price']) * item['quantity']:.2f}"
            for item in order["items"]
        )
        payment_status = order.get("payment_status", "Not Done")
        
        body = f"""
        Dear {user_info["name"]},

        Thank you for your order! Below are the details of your purchase:

        Order Number: {order_number}
        Items:
        {items_summary}
        Total: {currency_symbol}{total:.2f}
        Payment Status: {payment_status}
        Delivery Address: {user_info["address"]}
        Estimated Delivery: {order["delivery_date"]}

        We will notify you once your order is shipped.

        Best regards,
        Super Market Team
        """
        
        msg.attach(MIMEText(body, "plain"))

        # Connect to SMTP server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Enable TLS
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(sender, recipient, msg.as_string())
        
    except Exception as e:
        print(f"Failed to send email: {e}")
        from tkinter import messagebox
        messagebox.showwarning("Warning", "Order placed, but failed to send confirmation email.")

def send_payment_completion_email(order, user_info, currency, usd_to_inr, order_number):
    """
    Send a payment completion email to the user.
    
    Args:
        order (dict): Order details containing items, total, and delivery date.
        user_info (dict): User information including name, email, and address.
        currency (str): Currency used ('INR' or 'USD').
        usd_to_inr (float): Conversion rate from USD to INR.
        order_number (int): Unique order number.
    """
    try:
        # Prepare email content
        subject = f"Payment Confirmation - Order #{order_number}"
        sender = SMTP_USER
        recipient = user_info["email"]
        
        # Create MIME message
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = recipient
        msg["Subject"] = subject

        # Format order details
        currency_symbol = "$" if currency == "USD" else "₹"
        total = order["total"] / usd_to_inr if currency == "USD" else order["total"]
        items_summary = "\n".join(
            f"{item['item']['name']} x{item['quantity']} - {currency_symbol}{(item['item']['price'] / usd_to_inr if currency == 'USD' else item['item']['price']) * item['quantity']:.2f}"
            for item in order["items"]
        )
        
        body = f"""
        Dear {user_info["name"]},

        Thank you for completing the payment for your order! Below are the details:

        Order Number: {order_number}
        Items:
        {items_summary}
        Total: {currency_symbol}{total:.2f}
        Payment Status: Done
        Delivery Address: {user_info["address"]}
        Estimated Delivery: {order["delivery_date"]}

        Your order is now fully paid and will be processed for delivery.

        Best regards,
        Super Market Team
        """
        
        msg.attach(MIMEText(body, "plain"))

        # Connect to SMTP server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Enable TLS
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(sender, recipient, msg.as_string())
        
    except Exception as e:
        print(f"Failed to send payment completion email: {e}")
        from tkinter import messagebox
        messagebox.showwarning("Warning", "Payment completed, but failed to send confirmation email.")