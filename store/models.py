from django.db import models
from category.models import Category
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    product_name=models.CharField(max_length=200,unique=True)
    slug =models.SlugField(max_length=200,unique=True)
    description= models.TextField(max_length=500, blank=True)
    price  = models.IntegerField()
    images =models.ImageField(upload_to='photos/products')
    stock =models.IntegerField()
    is_available =models.BooleanField(default=True)
    category =models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date =models.DateTimeField(auto_now_add=True)
    modified_date =models.DateField(auto_now=True)
    anasayfa=models.BooleanField(default=False)
    seo_title=models.CharField(max_length=155,blank=True,null=True)
    seo_description=models.TextField(blank=True,null=True)
    


    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])

    def __str__(self):
        return self.product_name

    
class ProductGallery(models.Model):
    product =models.ForeignKey(Product,on_delete=models.CASCADE)
    image =models.ImageField(upload_to='photos/products',max_length=255)
    

    def __str__(self):
        return self.product.product_name
 
    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'




class Slider(models.Model):
    title = models.CharField(max_length=100, verbose_name='Başlık')
    description = models.TextField(blank=True, verbose_name='Açıklama')
    image = models.ImageField(upload_to='slider_images/', verbose_name='Görsel')
    link = models.URLField(blank=True, null=True, verbose_name='Buton Linki')  # Opsiyonel buton linki
    order = models.IntegerField(default=0, verbose_name='Sıra Numarası')  # Slider'lar sıralı olsun

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']  # Slider'lar sırasıyla listelenecek
