from .models import CartItem, Cart
from .utils import _cart_id


def counter(request):
    cart_count = 0

    if 'admin' in request.path:
        return {}

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    else:
        cart = Cart.objects.filter(cart_id=_cart_id(request)).first()
        cart_items = CartItem.objects.filter(cart=cart) if cart else []

    for item in cart_items:
        cart_count += item.quantity

    return {'cart_count': cart_count}
