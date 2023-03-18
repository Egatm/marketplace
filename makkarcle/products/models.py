from django.db import models
from django.urls import reverse
from django.conf import settings


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
	category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name="Категория")
	firma = models.CharField(max_length=100, blank=True, verbose_name="Производитель")
	name = models.CharField(max_length=150, db_index=True, verbose_name="Название")
	image = models.ImageField(upload_to='images/', default="images/no_image.jpg", blank=True, verbose_name="Изображение")
	description = models.TextField(max_length=1000, blank=True, verbose_name="Краткое описание")
	description_all = models.TextField(max_length=2000, blank=True, verbose_name="Полное описание")
	price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Цена")
	available = models.BooleanField(default=True)

	# seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	class Meta:
		ordering = ('name',)
		verbose_name = 'Товар'
		verbose_name_plural = 'Товары'


	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse("product_list")


class ProductPhoto(models.Model):
	photo = models.ImageField(upload_to='products/', blank=True, verbose_name="Изображение")
	product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Comment(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор")
	product = models.ForeignKey(Product, on_delete=models.CASCADE, )
	comment = models.CharField(max_length=200, verbose_name="Отзыв")

	class Meta:
		verbose_name = "Отзыв"
		verbose_name_plural = 'Отзывы'

	def __str__(self):
		return self.comment

	def get_absolute_url(self):
		return reverse("product_list")
