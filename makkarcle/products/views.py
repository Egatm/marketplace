from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView

from .models import Product
# from .forms import CommentForm


class ProductsCreateView(CreateView):
    model = Product
    template_name = "product_new.html"
    fields = (
        "category",
        "name",
        "firma",
        "description",
        "description_all",
        "image",
        "price",
    )


class ProductsListView(ListView):
    model = Product
    template_name = "product_list.html"


class ProductsDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'] = CommentForm()
    #     return context


class ProductsUpdateView(UpdateView):
    model = Product
    fields = (
        "firma",
        "name",
        "image",
        "description",
        "description_all",
        "price",
    )
    template_name = "product_edit.html"


class ProductsDeleteView(DeleteView):
    model = Product
    template_name = "product_delete.html"
    success_url = reverse_lazy("product_list")
