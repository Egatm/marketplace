from django.urls import path
# from .views import product_list
from .views import ProductsListView

urlpatterns = [
    # path('product/', product_list, name='product_list'),
    path("", ProductsListView.as_view(), name="product_list")
]
