from django.shortcuts import render, redirect
from django.http import HttpResponse
from carts.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order,OrderProduct
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


def place_order(request, total=0, quantity=0):
    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    
    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity

    tax = total * 0.02
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Sipariş bilgilerini kaydetme
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.user = current_user  # Kullanıcıyı siparişle ilişkilendirme
            data.save()

            # Sipariş numarası oluşturma
            current_date = datetime.date.today().strftime("%Y%m%d")
            order_number = f"{current_date}{data.id}"
            data.order_number = order_number
            data.save()
            
            


            for item in cart_items:
                order_product = OrderProduct()
                order_product.order = data
                order_product.user = current_user
                order_product.product = item.product
                order_product.quantity = item.quantity
                order_product.product_price = item.product.price
                order_product.ordered = True  # Ürün artık sipariş edildi
                order_product.save()

                # Sepetteki ürünü silme
            CartItem.objects.filter(user=current_user).delete()  # Sepeti temizle

        # Sipariş oluşturulduktan sonra kullanıcıya mesaj gönderme
        mail_subject = 'Siparişiniz başarıyla oluşturuldu'
        message = render_to_string('orders/order_recieved_email.html', {
                'user': request.user,
                'order': data,

                
              
            })
        to_email=request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

        messages.success(request, "Siparişiniz başarıyla oluşturuldu.")
        return redirect('order_complete')

    return redirect('checkout')

def order_complete(request):
    return render(request, 'orders/order_complete.html')

