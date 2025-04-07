from django.shortcuts import render,get_object_or_404
from .models import Product,ProductGallery
from category.models import Category
from carts.views import _cart_id
from django.db.models import Q


from carts.models import cartItem
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator



def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug is not None:
        # Kategoriye göre ürünleri filtrele
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator=Paginator(products,9)#paginate sayfası gösterilecek ürün sayısı kategoride
        page=request.GET.get('page')
        paged_products =paginator.get_page(page)
        product_count = products.count()
    else:
        # Kategorisiz tüm mevcut ürünleri listele
        products = Product.objects.filter(is_available=True).order_by('id')
        paginator=Paginator(products,9)#store pagination ürün sayfası
        page=request.GET.get('page')
        paged_products =paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': paged_products,  # Ürünleri templatene gönder normalde product,paginate işlem yüzünden
        'product_count': product_count,  # Ürün sayısını templatene gönder
        'category': categories  # Eğer kategori filtresi varsa, kategoriyi de templatene gönder
    }

    return render(request, 'store/store.html', context)

def product_detail(request,category_slug,product_slug):
    try:
        single_product=Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart =cartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    
    except Exception as e:
        raise e
    
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context  ={
        'single_product':single_product,
        'in_cart'        :in_cart,
        'product_gallery' :product_gallery,
    }    
    return render(request,'store/product_detail.html',context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword )| Q(product_name__icontains=keyword))
            product_count = products.count()
            context = {
                'products': products,
                'product_count': product_count,
             
            }   
    return render(request,'store/store.html',context)
