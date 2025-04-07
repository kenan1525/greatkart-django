from django.contrib import admin
from .models import Order, OrderProduct, Payment


class OrderProductInline(admin.TabularInline):    
    model=OrderProduct
    readonly_fields=('payment','user','product','quantity','product_price','ordered')
    extra=0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'first_name', 'last_name', 'status', 'is_ordered', 'created_at')
    list_filter = ('status', 'is_ordered')
    search_fields = ('order_number', 'first_name', 'email')
    list_per_page=20
    inlines=[OrderProductInline]

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'user', 'created_at')
    list_filter = ('order', 'product')
    search_fields = ('order__order_number', 'product__product_name', 'user__email')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(Payment)