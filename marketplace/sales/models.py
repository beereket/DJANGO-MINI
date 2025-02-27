from django.db import models
from django.conf import settings
from users.models import User
from products.models import Product

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.BooleanField(default=False)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment by {self.user.username} - {self.amount}"

class OrderHistory(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders_history")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sold_products")
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}: {self.product.name} x {self.quantity} (Buyer: {self.buyer.username})"