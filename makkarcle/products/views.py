from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from .models import Product
from .forms import CommentForm


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
