from django.db import models
from users.models import User
from products.models import Product

class TradeOffer(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trade_offers")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.seller.username} is selling {self.product.name} for {self.price}"
