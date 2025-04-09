from django.shortcuts import render
from store.models import Product, Slider


def home(request):
    products =Product.objects.all().filter(anasayfa=True)
    sliders = Slider.objects.all()
    context ={
        'products':products,
        'sliders':sliders,
    }

    return render(request,'home.html',context)

def about(request):
    return render(request,'about.html')