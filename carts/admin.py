from django.contrib import admin
from .models import Cart,cartItem

# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id','data_added')

class cartItemAdmin(admin.ModelAdmin):
    list_display = ('product','cart','quantity','is_active')



admin.site.register(Cart,CartAdmin)
admin.site.register(cartItem,cartItemAdmin)


