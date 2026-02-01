from django.conf import settings
from django.db import models
from store.models import Product


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    cart_id = models.CharField(max_length=250, null=True, blank=True, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) if self.user else self.cart_id



class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product} - {self.quantity}"
