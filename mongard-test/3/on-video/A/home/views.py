from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Category , Product

class HomeView(View):
    template_name = 'home/home.html'

    def get(self , request):
        products = Product.objects.filter(available=True)
        return render(request , self.template_name , {'products' : products})


class ProductDetailView(View):
    template_name = 'home/detail.html'

    def get(self , request , product_slug):
        product = get_object_or_404(Product , slug = product_slug)
        return render(request , self.template_name , {'product' : product})