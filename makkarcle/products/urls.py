from django.urls import path
# from .views import product_list
from .views import ProductsListView, ProductsDetailView, ProductCreateView, ProductsUpdateView, ProductsDeleteView
from . import views

urlpatterns = [
    path("", ProductsListView.as_view(), name="product_list"),
    path("<int:pk>/", ProductsDetailView.as_view(), name="product_detail"),
    path("add/", ProductCreateView.as_view(), name="product_new"),
    path("<int:pk>/edit/", ProductsUpdateView.as_view(), name="product_edit"),
    path("<int:pk>/delete/", ProductsDeleteView.as_view(), name="product_delete"),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/<int:pk>/change_quantity/', views.change_quantity, name='change_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('my_orders/', views.my_orders, name='my_orders'),
]
