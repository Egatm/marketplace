from django.views.generic import TemplateView
from products.models import Product


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_products = Product.objects.order_by('-id')[:3]
        context['last_products'] = last_products
        return context
