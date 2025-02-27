from django.db import models
from users.models import User
from products.models import Product
from trading.models import TradeOffer

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    trade_offer = models.ForeignKey(TradeOffer, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.product:
            return f"{self.user.username} added {self.product.name} to cart"
        if self.trade_offer:
            return f"{self.user.username} added trade offer {self.trade_offer.id} to cart"
