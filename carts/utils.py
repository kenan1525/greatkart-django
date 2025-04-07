import uuid
from carts.models import Cart, cartItem

def _cart_id(request):
    """Kullanıcı giriş yapmışsa kendi ID'si, yoksa session ID kullan."""
    if request.user.is_authenticated:
        return str(request.user.id)
    if not request.session.get('cart_id'):
        request.session['cart_id'] = str(uuid.uuid4())
    return request.session['cart_id']


def get_or_create_cart(request):
    """Kullanıcının sepetini getir veya anonim sepet oluştur."""
    user = request.user if request.user.is_authenticated else None
    cart_id = _cart_id(request)
    cart, _ = Cart.objects.get_or_create(user=user, cart_id=cart_id)
    return cart


def merge_carts(request, user):
    """Anonim sepeti, giriş yapan kullanıcının sepetiyle birleştirir."""
    session_cart_id = request.session.get('saved_cart_id')
    if not session_cart_id:
        return
    
    guest_cart = Cart.objects.filter(cart_id=session_cart_id).first()
    if not guest_cart:
        request.session.pop('cart_id', None)
        return

    user_cart, _ = Cart.objects.get_or_create(user=user)

    if guest_cart.id == user_cart.id:
        return

    guest_cart_items = guest_cart.cartitem_set.all()
    for item in guest_cart_items:
        existing_item = user_cart.cartitem_set.filter(product=item.product).first()
        if existing_item:
            existing_item.quantity += item.quantity
            existing_item.save()
            item.delete()
        else:
            item.cart = user_cart
            item.user = user
            item.is_active = True
            item.save()

    guest_cart.delete()
    request.session['cart_id'] = str(user_cart.cart_id)
