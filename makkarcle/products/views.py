from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from datetime import date
from .models import Product, ProductPhoto, Order
from .forms import CommentForm, ProductPhotoForm, ProductForm
from .filters import ProductFilter
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages


ProductPhotoFormSet = inlineformset_factory(Product, ProductPhoto, form=ProductPhotoForm, extra=1, can_delete=False)


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_new.html'

    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ProductPhotoFormSet(self.request.POST, self.request.FILES, prefix='productphoto')
        else:
            context['formset'] = ProductPhotoFormSet(queryset=ProductPhoto.objects.none(), prefix='productphoto')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ProductsListView(ListView):
    model = Product
    template_name = "product_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('search')
        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(description__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = date.today()

        products = self.get_queryset()
        my_filter = ProductFilter(self.request.GET, queryset=products)

        if my_filter.form.is_valid():
            products = my_filter.qs
        context['product_list'] = products
        context['filter'] = my_filter

        return context


class CommentGet(DetailView):
    model = Product
    template_name = "product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class CommentPost(SingleObjectMixin, FormView):
    model = Product
    form_class = CommentForm
    template_name = "product_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.product = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        product = self.get_object()
        return reverse("product_detail", kwargs={"pk": product.pk})


class ProductsDetailView(View):
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)


class ProductsUpdateView(UpdateView):
    model = Product
    fields = (
        "category",
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


@login_required
def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    order, created = Order.objects.get_or_create(
         user=request.user,
         product=product,
         defaults={'quantity': 1}
    )
    if not created:
        order.quantity += 1
        order.save()
    messages.success(request, "Товар добавлен в корзину.")
    return redirect('cart')


@login_required
def cart(request):
    orders = Order.objects.filter(user=request.user)
    context = {'orders': orders}
    return render(request, 'cart.html', context)


@login_required
def remove_from_cart(request, id):
    order = Order.objects.get(id=id)
    order.delete()
    messages.success(request, "Товар удален из корзины.")
    return redirect('cart')


def change_quantity(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        new_quantity = request.POST.get('quantity')
        if int(new_quantity) > 0:
            order.quantity = int(new_quantity)
            order.save()
    return redirect('cart')


def calculate_cart_price(orders):
    total_price = 0
    for order in orders:
        total_price += order.product.price * order.quantity
    return total_price


def view_cart(request):
    orders = Order.objects.filter(user=request.user, is_ordered=False)

    if not orders.exists():
        return render(request, 'cart.html', {'message': 'Ваша корзина пуста.'})

    total_price = round(calculate_cart_price(orders), 2)
    context = {
        'orders': orders,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)
