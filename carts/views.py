
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from store.models import Product
from carts.utils import get_or_create_cart, merge_carts
from carts.models import cartItem, Cart
from django.db.models import F
from carts.utils import get_or_create_cart, _cart_id
from django.core.exceptions import ObjectDoesNotExist

from orders.forms import OrderForm





def debug_cart_session(request):
    print("🔹 Session cart_id:", request.session.get("cart_id"))
    print("🔹 Kullanıcı:", request.user)
    print("🔹 Giriş yapmış mı:", request.user.is_authenticated)

def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)
    
    cart_item, created = cartItem.objects.get_or_create(
        product=product, cart=cart,
        defaults={'quantity': 1, 'user': request.user if request.user.is_authenticated else None}
    )
    
    if not created:
        cart_item.quantity = F('quantity') + 1
        cart_item.save(update_fields=['quantity'])
        cart_item.refresh_from_db()  # Güncellenmiş değeri çek
    
    return redirect('cart')

def remove_cart(request, product_id):
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(cartItem, product_id=product_id, cart=cart)
    
    if cart_item.quantity > 1:
        cart_item.quantity = F('quantity') - 1
        cart_item.save(update_fields=['quantity'])
        cart_item.refresh_from_db()
    else:
        cart_item.delete()

    return redirect('cart')

def remove_cart_item(request, product_id):
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(cartItem, product_id=product_id, cart=cart)
    cart_item.delete()
    messages.success(request, "Ürün sepetten kaldırıldı.")
    return redirect('cart')

def cart(request):
    cart = get_or_create_cart(request)
    cart_items = cartItem.objects.filter(cart=cart, is_active=True)
    total = sum(item.product.price * item.quantity for item in cart_items)
    tax = total * 0.02
    return render(request, 'store/cart.html', {'total': total, 'tax': tax, 'grand_total': total + tax, 'cart_items': cart_items})

# @login_required(login_url='login')
# def checkout(request):
#     cart = get_or_create_cart(request)
#     cart_items = cartItem.objects.filter(cart=cart, is_active=True)
#     total = sum(item.product.price * item.quantity for item in cart_items)
#     tax = total * 0.02
#     return render(request, 'store/checkout.html', {
#         'total': total, 
#         'tax': tax, 
#         'grand_total': total + tax, 
#         'cart_items': cart_items
#     })



# @login_required(login_url='login')
# def checkout(request):
#     # Kullanıcıya ait sepeti alıyoruz (anonimse sepeti oluşturuyoruz)
#     cart = get_or_create_cart(request)

#     # Sepetteki ürünleri alıyoruz ve aktif ürünleri filtreliyoruz
#     cart_items = cartItem.objects.filter(cart=cart, is_active=True)

#     # Toplam fiyatı hesaplıyoruz
#     total = sum(item.product.price * item.quantity for item in cart_items)

#     # Vergi hesaplaması
#     tax = total * 0.02  # Örneğin %2 vergi

#     # Grand total (vergi dahil toplam)
#     grand_total = total + tax

#     # Formu işleme alıyoruz
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             # Sipariş formu geçerli ise kaydediyoruz
#             order = form.save(commit=False)
#             order.cart = cart  # Sepet ile ilişkilendiriyoruz
#             order.user = request.user  # Giriş yapan kullanıcıyı atıyoruz
#             order.save()

#             # Sepetindeki ürünleri işaretliyoruz
#             cart_items.update(is_active=False)

#             # Sepeti boşaltıyoruz
#             cart.cartitem_set.all().delete()

#             # Başarıyla sipariş sonrası yönlendirme
#             return redirect('order_complete')  # Sipariş tamamlandıktan sonra bir sayfaya yönlendirebilirsiniz.

#     else:
#         form = OrderForm()  # Eğer GET isteği ise formu boş olarak gönderiyoruz

#     # Şablona gerekli verileri gönderiyoruz
#     return render(request, 'store/checkout.html', {
#         'total': total, 
#         'tax': tax, 
#         'grand_total': grand_total, 
#         'cart_items': cart_items,
#         'form': form
#     })
# @login_required(login_url='login')
# def checkout(request):
#     # Kullanıcıya ait sepeti alıyoruz (anonimse sepeti oluşturuyoruz)
#     cart = get_or_create_cart(request)

#     # Sepetteki ürünleri alıyoruz ve aktif ürünleri filtreliyoruz
#     cart_items = cartItem.objects.filter(cart=cart, is_active=True)

#     # Toplam fiyatı hesaplıyoruz
#     total = sum(item.product.price * item.quantity for item in cart_items)

#     # Vergi hesaplaması
#     tax = total * 0.02  # Örneğin %2 vergi

#     # Grand total (vergi dahil toplam)
#     grand_total = total + tax

#     # Formu işleme alıyoruz
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             # Sipariş formu geçerli ise kaydediyoruz
#             order = form.save(commit=False)
#             order.cart = cart  # Sepet ile ilişkilendiriyoruz
#             order.user = request.user  # Giriş yapan kullanıcıyı atıyoruz
#             order.save()

#             # Sepetindeki ürünleri işaretliyoruz
#             cart_items.update(is_active=False)

#             # Sepeti boşaltıyoruz
#             cart.cartitem_set.all().delete()

#             # Başarıyla sipariş sonrası yönlendirme
#             return redirect('order_complete')  # Sipariş tamamlandıktan sonra bir sayfaya yönlendirebilirsiniz.

#     else:
#         form = OrderForm()  # Eğer GET isteği ise formu boş olarak gönderiyoruz

#     # Şablona gerekli verileri gönderiyoruz
#     return render(request, 'store/checkout.html', {
#         'total': total, 
#         'tax': tax, 
#         'grand_total': grand_total, 
#         'cart_items': cart_items,
#         'form': form
#     })
@login_required(login_url='login')
def checkout(request):
    # Kullanıcıya ait sepeti alıyoruz (anonimse sepeti oluşturuyoruz)
    cart = get_or_create_cart(request)

    # Sepetteki ürünleri alıyoruz ve aktif ürünleri filtreliyoruz
    cart_items = cartItem.objects.filter(cart=cart, is_active=True)

    # Toplam fiyatı hesaplıyoruz
    total = sum(item.product.price * item.quantity for item in cart_items)

    # Vergi hesaplaması
    tax = total * 0.02  # Örneğin %2 vergi

    # Grand total (vergi dahil toplam)
    grand_total = total + tax

    # Formu işleme alıyoruz
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Sipariş formu geçerli ise kaydediyoruz
            order = form.save(commit=False)
            order.cart = cart  # Sepet ile ilişkilendiriyoruz
            order.user = request.user  # Giriş yapan kullanıcıyı atıyoruz
            order.save()

            # Sepetindeki ürünleri işaretliyoruz
            cart_items.update(is_active=False)

            # Sepeti boşaltıyoruz
            cart.cartitem_set.all().delete()

            # Başarıyla sipariş sonrası yönlendirme
            return redirect('order_complete')  # Sipariş tamamlandıktan sonra bir sayfaya yönlendirebilirsiniz.

    else:
        form = OrderForm()  # Eğer GET isteği ise formu boş olarak gönderiyoruz

    # Şablona gerekli verileri gönderiyoruz
    return render(request, 'store/checkout.html', {
        'total': total, 
        'tax': tax, 
        'grand_total': grand_total, 
        'cart_items': cart_items,
        'form': form
    })
