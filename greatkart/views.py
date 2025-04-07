from django.shortcuts import render
from store.models import Product


def home(request):
    products =Product.objects.all().filter(anasayfa=True)
    context ={
        'products':products,
    }

    return render(request,'home.html',context)

def about(request):
    return render(request,'about.html')