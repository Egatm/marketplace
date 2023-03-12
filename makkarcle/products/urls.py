from django.urls import path
# from .views import product_list
from .views import ProductsListView, ProductsDetailView, ProductsCreateView

urlpatterns = [
    path("", ProductsListView.as_view(), name="product_list"),
    path("<int:pk>/", ProductsDetailView.as_view(), name="product_detail"),
    path("add/", ProductsCreateView.as_view(), name="product_new"),
]
