from django.db import models
from django.conf import settings
from menu.models import Pizza, Topping
from menu.models import Pizza, Topping


class Order(models.Model):
    STATUS_CHOICES = [
        ('P', 'Placed'),
        ('B', 'Being Prepared'),
        ('R', 'Ready for Pickup'),
        ('D', 'Delivered'),
        ('C', 'Cancelled'),
    ]
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=50)  # TODO: this should be replaced with proper FK to "accounts"

    def __str__(self):
        return f"Order {self.id} by {self.customer_name}"  # TODO: should be self.user.username in a real scenario...


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    toppings = models.ManyToManyField(Topping, blank=True)

    def __str__(self):
        return f"Item {self.id} of Order {self.order.id}"
