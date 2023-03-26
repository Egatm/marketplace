from django.test import TestCase
from django.urls import reverse
from products.models import Product, Category
from accounts.models import CustomUser


# Create your tests here.
class HomePageTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="TestCategory")
        self.user = CustomUser.objects.create_user(username='test', password='test123456')
        self.product = Product.objects.create(
            name='Test Product',
            price=9.99,
            seller=self.user,
            category=self.category,
            available=True
        )

    def test_url_exists_at_correct_location_homepage(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_homepage_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertContains(response, "Home")

        # Check if last_products are in the context
        last_products = response.context['last_products']
        expected_data = list(Product.objects.order_by('-id')[:3])
        self.assertListEqual(list(last_products), expected_data)
