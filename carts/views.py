from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from store.models import Product
from .models import Cart, CartItem
from .utils import get_or_create_cart


# ----------------------
# Helper Fonksiyonlar
# ----------------------
def _get_cart_items(request):
    """
    Kullanıcının sepet öğelerini döndürür.
    Login olmuşsa kullanıcı bazlı,
    değilse session bazlı.
    """
    cart = get_or_create_cart(request, request.user)

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(cart=cart, user=request.user, is_active=True)
    else:
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

    return cart_items


# ----------------------
# Cart Actions
# ----------------------
def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request, request.user)

    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            cart=cart,
            user=request.user
        )
    else:
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            cart=cart
        )

    if not created:
        cart_item.quantity += 1

    cart_item.save()
    return redirect('cart')


def remove_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request, request.user)

    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, cart=cart, product=product, user=request.user)
    else:
        cart_item = get_object_or_404(CartItem, cart=cart, product=product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')


def remove_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request, request.user)

    if request.user.is_authenticated:
        CartItem.objects.filter(cart=cart, product=product, user=request.user).delete()
    else:
        CartItem.objects.filter(cart=cart, product=product).delete()

    return redirect('cart')


# ----------------------
# Cart Display
# ----------------------
def cart(request):
    cart_items = _get_cart_items(request)
    total = sum(item.product.price * item.quantity for item in cart_items)
    quantity = sum(item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
    }
    return render(request, 'store/cart.html', context)


# ----------------------
# Checkout
# ----------------------
@login_required(login_url='login')
def checkout(request):
    cart_items = _get_cart_items(request).filter(user=request.user)

    if not cart_items.exists():
        messages.warning(request, "Sepetiniz boş.")
        return redirect('store')

    total = sum(item.product.price * item.quantity for item in cart_items)
    quantity = sum(item.quantity for item in cart_items)

    from orders.forms import OrderForm
    form = OrderForm()

    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'form': form,
    }

    return render(request, 'store/checkout.html', context)
