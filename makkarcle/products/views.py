from django.shortcuts import render
from .models import Product
from .forms import ProductForm


def product_list(request):
    products = Product.objects.all()
    form = ProductForm()

    context = {'products': products, 'form': form}

    return render(request, 'products/product_list.html', context)

