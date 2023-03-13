from django.urls import path
# from .views import product_list
from .views import ProductsListView, ProductsDetailView, ProductsCreateView, ProductsUpdateView, ProductsDeleteView

urlpatterns = [
    path("", ProductsListView.as_view(), name="product_list"),
    path("<int:pk>/", ProductsDetailView.as_view(), name="product_detail"),
    path("add/", ProductsCreateView.as_view(), name="product_new"),
    path("<int:pk>/edit/", ProductsUpdateView.as_view(), name="product_edit"),
    path("<int:pk>/delete/", ProductsDeleteView.as_view(), name="product_delete"),
]
