from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from carts.utils import merge_carts


@receiver(user_logged_in)
def merge_cart_after_login(sender, request, user, **kwargs):
    merge_carts(request, user)
