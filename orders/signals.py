from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Order, OrderItem
from django.conf import settings
from django.dispatch import Signal

order_confirmed = Signal()

@receiver(pre_save, sender=Order)
def check_status_change(sender, instance, **kwargs):
    if instance.pk:  
        previous = Order.objects.get(pk=instance.pk)
        new_status = instance.status
        
        if previous.status != new_status:
            order = Order.objects.get(pk=instance.pk)
            send_mail(
                subject=f"Order #{order.id} Status Updated",
                message=f"Hello {order.user.username},\n\nYour order #{order.id} status has been updated to '{new_status}'.\n\nBest regards,\nYour Bookstore Team",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[order.user.email],
                fail_silently=False,
            )

@receiver(order_confirmed)
def send_order_confirmation_email(sender, order, user, **kwargs):

    order_items = OrderItem.objects.filter(order=order)
    item_details = "\n".join([f"{item.quantity} x {item.book.title} at ${item.price}" for item in order_items])
    subject = f"Order Confirmation - Order #{order.id}"
    message = f"""
    Hello {user.username},

    Total Amount: $ {order.total_amount}
    Thank you for your order! Your order #{order.id} has been successfully placed on {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}.
    Order Details:
    {item_details}

    We will notify you once your order is shipped.

    Best regards,
    Your Bookstore Team
    """

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email, "f219070@cfd.nu.edu.pk"],
        fail_silently=False,
    )