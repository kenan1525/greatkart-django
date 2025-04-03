from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from carts.utils import merge_carts

@receiver(user_logged_in)
def preserve_cart_id_before_login(sender, request, user, **kwargs):
    """Kullanıcı giriş yapmadan önce oturumdaki cart_id'yi sakla"""
    if "cart_id" in request.session:
        # Kullanıcının anonim sepeti varsa, bunu geçici olarak kaydediyoruz.
        request.session["saved_cart_id"] = request.session["cart_id"]
        print(f"🔹 Cart ID, giriş öncesi kaydedildi: {request.session['saved_cart_id']}")

@receiver(user_logged_in)
def merge_carts_after_login(sender, request, user, **kwargs):
    """Kullanıcı giriş yaptıktan sonra anonim sepeti kullanıcı sepetiyle birleştir"""
    session_cart_id = request.session.get("saved_cart_id")
    print(f"🔹 Girişten sonra kayıtlı cart_id: {session_cart_id}")

    if session_cart_id:
        # Misafir sepetini, kullanıcı sepetine birleştiriyoruz
        merge_carts(request, user)
        
        # Giriş yapıldıktan sonra, geçici kaydı temizliyoruz
        request.session["saved_cart_id"] = None
        print(f"🔹 Cart ID, birleştirme işleminden sonra temizlendi.")


