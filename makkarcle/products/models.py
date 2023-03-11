from django.db import models
from django.urls import reverse


# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=100, db_index=True)

	class Meta:
		ordering = ('name',)
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'

	def __str__(self):
		return self.name


class Product(models.Model):
	category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
	name = models.CharField(max_length=150, db_index=True)
	image = models.ImageField(upload_to='images/', default="images/no_image.jpg", blank=True)
	description = models.TextField(max_length=1000, blank=True)
	price = models.DecimalField(max_digits=6, decimal_places=2)
	available = models.BooleanField(default=True)

	class Meta:
		ordering = ('name',)
		verbose_name = 'Товар'
		verbose_name_plural = 'Товары'

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse("product_list", kwargs={"pk": self.pk})
