from .models import Cart, CartItem


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def get_or_create_cart(request, user=None):
    if user and user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=user)
    else:
        cart_id = _cart_id(request)
        cart, created = Cart.objects.get_or_create(cart_id=cart_id)
    return cart


def merge_carts(request, user):
    try:
        session_cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        return

    user_cart, created = Cart.objects.get_or_create(user=user)

    session_items = CartItem.objects.filter(cart=session_cart)

    for item in session_items:
        cart_item, created = CartItem.objects.get_or_create(
            cart=user_cart,
            product=item.product,
            user=user
        )

        if not created:
            cart_item.quantity += item.quantity

        cart_item.save()

    # session cart sil
    session_cart.delete()
