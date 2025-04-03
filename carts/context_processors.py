# from .models import Cart,cartItem
# from .views import _cart_id


# def counter(request):
#     cart_count=0
#     if 'admin' in request.path:
#         return {}
#     else:
#         try:
#             cart =Cart.objects.filter(cart_id=_cart_id(request))
#             if request.user.is_authenticated:
#                 cart_items = cartItem.objects.all().filter(user=request.user)
#             else:
#                 cart_items = cartItem.objects.all().filter(cart=cart[:1])
            
#             for cart_item in cart_items:
#                 cart_count += cart_item.quantity

#         except Cart.DoesNotExist:
#             cart_count=0
#     return dict(cart_count=cart_count)      
# from .models import Cart, cartItem

from .models import Cart, cartItem
from .views import _cart_id

def counter(request):
    cart_count = 0

    if 'admin' in request.path:
        return {}

    try:
        if request.user.is_authenticated:
            # Kullanıcı giriş yaptıysa, onun sepetine ait ürünleri al
            cart_items = cartItem.objects.filter(cart__user=request.user)
        else:
            # Giriş yapmamış kullanıcı için session bazlı sepeti al
            cart = Cart.objects.filter(cart_id=_cart_id(request)).first()
            if cart:
                cart_items = cartItem.objects.filter(cart=cart)
            else:
                cart_items = []

        # Sepetteki ürünlerin toplam miktarını hesapla
        for cart_item in cart_items:
            cart_count += cart_item.quantity

    except Cart.DoesNotExist:
        cart_count = 0

    return {"cart_count": cart_count}
