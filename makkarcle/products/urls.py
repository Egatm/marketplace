from django.urls import path
# from .views import product_list
from .views import ProductsListView, ProductsDetailView

urlpatterns = [
    path("", ProductsListView.as_view(), name="product_list"),
    path("<int:pk>/", ProductsDetailView.as_view(), name="product_detail"),
]
