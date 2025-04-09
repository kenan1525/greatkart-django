"""greatkart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('kenan/', admin.site.urls),  # Admin paneli için URL
    path('', views.home, name='home'),  # Anasayfa URL
    path('about/', views.about, name='about'),  # Hakkında sayfası URL
    path('store/', include('store.urls')),  # Store (ürün) sayfası URL
    path('cart/', include('carts.urls')),  # Sepet sayfası URL
    path('accounts/', include('accounts.urls')),  # Hesap işlemleri için URL
    path('orders/', include('orders.urls')),  # Sipariş sayfası URL
]

# Eğer DEBUG modu açıksa, medya ve statik dosyaların doğru şekilde yüklenmesini sağlamak için:
if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Medya dosyaları
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # Statik dosyalar
