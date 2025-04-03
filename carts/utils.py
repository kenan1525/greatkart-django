import uuid

def _cart_id(request):
    """Kullanıcı giriş yapmışsa kendi ID'si, yoksa session ID kullan."""
    if request.user.is_authenticated:
        return str(request.user.id)  # Kullanıcı ID'sini döndür
    if not request.session.get('cart_id'):
        request.session['cart_id'] = str(uuid.uuid4())  # Yeni bir cart ID oluştur
    return request.session['cart_id']

from carts.models import Cart

def get_or_create_cart(request):
    """Kullanıcının sepetini getir veya anonim sepet oluştur."""
    user = request.user if request.user.is_authenticated else None
    cart_id = _cart_id(request)
    
    # Eğer kullanıcı anonimse, Cart'ı user=None olarak oluşturmalıyız
    cart, created = Cart.objects.get_or_create(user=user, cart_id=cart_id)

    if created:
        print(f"🛒 Yeni sepet oluşturuldu: {cart_id}")
    else:
        print(f"✔️ Sepet zaten var: {cart_id}")

    return cart

import logging
from carts.models import Cart, cartItem

logger = logging.getLogger(__name__)

def merge_carts(request, user):
    """Anonim kullanıcının sepetini giriş yapan kullanıcıya aktarır."""
    session_cart_id = request.session.get('cart_id')
    
    if not session_cart_id:
        logger.info("Giriş yapmadan önce kayıtlı cart_id bulunamadı.")
        return
    
    guest_cart = Cart.objects.filter(cart_id=session_cart_id).first()
    
    if not guest_cart:
        logger.warning(f"Misafir sepeti bulunamadı: {session_cart_id}")
        request.session.pop('cart_id', None)  # Geçersiz cart_id'yi temizle
        return  

    # Kullanıcının mevcut sepetini getir
    user_cart = Cart.objects.filter(user=user).first()

    if not user_cart:
        user_cart = guest_cart
        user_cart.user = user
        user_cart.save()
        request.session['cart_id'] = str(user_cart.cart_id)
        logger.info(f"🛒 Misafir sepeti doğrudan kullanıcıya atandı: {user_cart.cart_id}")
        return
    
    if guest_cart.id == user_cart.id:
        logger.info(f"✅ Misafir sepeti zaten kullanıcıya ait: {user.email}")
        return  

    # Misafir sepetindeki tüm ürünleri kullanıcı sepetine taşı
    guest_cart_items = guest_cart.cartitem_set.all()
    for item in guest_cart_items:
        existing_item = user_cart.cartitem_set.filter(product=item.product).first()
        if existing_item:
            existing_item.quantity += item.quantity
            existing_item.save()
            item.delete()
            logger.info(f"✔️ Ürün miktarı artırıldı: {item.product.product_name}")
        else:
            item.cart = user_cart
            item.save()
            logger.info(f"🛒 Yeni ürün eklendi: {item.product.product_name}")

    # Misafir sepetini sil
    guest_cart.delete()
    logger.info(f"🚮 Misafir sepeti silindi: {session_cart_id}")

    request.session['cart_id'] = str(user_cart.cart_id)
    logger.info(f"✅ Sepet başarıyla birleştirildi: {user.email} için Yeni Sepet ID: {user_cart.cart_id}")

    # burda bitiyor...
