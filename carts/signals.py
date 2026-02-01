# from django.contrib.auth.signals import user_logged_in
# from django.dispatch import receiver
# from carts.utils import merge_carts


# @receiver(user_logged_in)
# def merge_carts_after_login(sender, request, user, **kwargs):
#     """
#     Kullanıcı login veya register olduktan sonra
#     session sepetini user sepetiyle birleştirir.
#     """
#     session_cart_id = request.session.get("cart_id")

#     if session_cart_id:
#         merge_carts(request, user)
#         del request.session["cart_id"]
