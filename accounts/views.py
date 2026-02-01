from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django import forms
from .models import Account

User = get_user_model()


# ============================
# Registration Form
# ============================
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'form-control'
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match!')

        # Email zaten kayıtlı mı kontrol
        email = cleaned_data.get('email')
        if email and Account.objects.filter(email=email).exists():
            self.add_error('email', 'Bu email zaten kayıtlı!')

        return cleaned_data


# ============================
# REGISTER
# ============================
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = True
            user.save()

            # Eğer guest cart varsa temizle
            if 'cart' in request.session:
                del request.session['cart']

            messages.success(request, 'Kayıt başarılı, giriş yapabilirsiniz')
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


# ============================
# LOGIN
# ============================
def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)

            # guest cart varsa temizle
            if 'cart' in request.session:
                del request.session['cart']

            return redirect('home')
        else:
            messages.error(request, 'Giriş başarısız')
            return redirect('login')

    return render(request, 'accounts/login.html')


# ============================
# LOGOUT
# ============================
def user_logout(request):
    logout(request)
    return redirect('login')


# ============================
# DASHBOARD / HOME
# ============================
@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/home.html')


# ============================
# ACCOUNT ACTIVATION
# ============================
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Hesabınız aktif edildi')
        return redirect('login')
    else:
        messages.error(request, 'Aktivasyon linki geçersiz')
        return redirect('register')


# ============================
# FORGOT PASSWORD
# ============================
def forgotPassword(request):
    return render(request, 'accounts/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    return render(request, 'accounts/resetPassword.html')


def resetPassword(request):
    return render(request, 'accounts/resetPassword.html')
