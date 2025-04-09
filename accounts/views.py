from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from carts.views import _cart_id
from carts.models import Cart, cartItem
from carts.utils import merge_carts
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.db import transaction


# logger = logging.getLogger(__name__)

def login_view(request):
    
    return render(request, "login.html")

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]

            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password
            )
            user.phone_number = phone_number
            user.save()

            # Kullanıcı aktivasyon maili gönderme
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            send_email = EmailMessage(mail_subject, message, to=[email])
            send_email.send()

            return redirect('/accounts/login/?command=verification&email=' + email)
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Kullanıcıyı doğrula (Burada custom authenticate kullanılmalı)
        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            # Kullanıcı giriş yaptıktan sonra sepete eklenen ürünleri korur  
            merge_carts(request, user)
            
            # Kullanıcının yeni sepet ID'sini güncelle
            user_cart = Cart.objects.filter(user=user).first()
            if user_cart:
                request.session['cart_id'] = str(user_cart.cart_id)
                # Logger'ı kaldırdık, log yazılmayacak
                # logger.info(f"🔄 Kullanıcı giriş yaptı, sepet ID güncellendi: {user_cart.cart_id}")
            else:
                # Eğer kullanıcıda sepet yoksa yeni sepet oluşturulacak
                # logger.warning(f"Sepet bulunamadı: {user.email}")
                user_cart = Cart.objects.create(user=user)
                request.session['cart_id'] = str(user_cart.cart_id)
                # logger.info(f"🛒 Yeni sepet oluşturuldu: {user_cart.cart_id}")
            
            return redirect('home')  # Kullanıcı giriş yaptıktan sonra anasayfaya yönlendir
        else:
            messages.error(request, 'Geçersiz giriş bilgileri')
            return render(request, 'accounts/login.html', {'exception_notes': 'Geçersiz giriş'})

    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def user_logout(request):
   auth.logout(request)  # Kullanıcı çıkış yapar
   messages.success(request, 'Başarıyla çıkış yaptınız')  # Başarı mesajı gösterilir
   return redirect('login')  # Giriş sayfasına yönlendirilir


def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):    
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'Hesabınız başarıyla etkinleştirildi!')
        return redirect('login')
    else:
        messages.error(request,'Geçersiz aktivasyon bağlantısı')
        return redirect('register')
    
@login_required(login_url='login')
def dashboard(request):
    return render(request,'accounts/dashboard.html')

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # PASSWORD RESET EMAIL
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'Password reset email has been sent to your email address')
            return redirect('login')
        else:
            messages.error(request,'Account does not exist')
            return redirect('forgotPassword')
    
    return render(request,'accounts/forgotPassword.html')

def resetpassword_validate(request,uidb64,token):
    try :
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):    
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request,'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request,'This link has expired')
        return redirect('login')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset successfully')
            return redirect('login')
        else:
            messages.error(request,'Password do not match')
            return redirect('resetPassword')
    else:
        return render(request,'accounts/resetPassword.html')
