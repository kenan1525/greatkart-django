import logging
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from carts.utils import merge_carts


from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from carts.utils import merge_carts

@receiver(user_logged_in)
def preserve_cart_id_before_login(sender, request, user, **kwargs):
    """Kullanıcı giriş yapmadan önce oturumdaki cart_id'yi sakla."""
    if "cart_id" in request.session:
        request.session["saved_cart_id"] = request.session["cart_id"]

@receiver(user_logged_in)
def merge_carts_after_login(sender, request, user, **kwargs):
    """Kullanıcı giriş yaptıktan sonra anonim sepeti kullanıcı sepetiyle birleştir."""
    session_cart_id = request.session.get("saved_cart_id")
    if session_cart_id:
        merge_carts(request, user)
        request.session["saved_cart_id"] = None

