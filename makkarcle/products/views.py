from django.views.generic import ListView, DetailView
from django.shortcuts import render
from .models import Product
from .forms import ProductForm


class ProductsListView(ListView):
    model = Product
    template_name = "product_list.html"

class ProductsDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
# def product_list(request):
#     products = Product.objects.all()
#     form = ProductForm()
#     context = {'products': products, 'form': form}
#     return render(request, 'product_list.html', context)
