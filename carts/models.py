from django.conf import settings  # Django'nun user modelini dinamik olarak almak için
from django.db import models
from store.models import Product

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # DÜZELTİLDİ
    data_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) if self.user else self.cart_id

class cartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # DÜZELTİLDİ
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product} - {self.quantity}"

