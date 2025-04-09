from django.contrib import admin
from .models import Product,ProductGallery, Slider
import admin_thumbnails

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display =('product_name','price','stock','category','modified_date','is_available')
    prepopulated_fields = {'slug':('product_name',)}
    inlines = [ProductGalleryInline]

from django.contrib import admin
from .models import Slider

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'image']
    search_fields = ['title']
    list_filter = ['order']

admin.site.register(Product,ProductAdmin)
admin.site.register(ProductGallery)

