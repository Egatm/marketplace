from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


# Create your models here.
class CustomUser(AbstractUser):
	birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
	email = models.EmailField(max_length=255, unique=True, verbose_name="Адрес электронной почты")
	is_seller = models.BooleanField(default=False, verbose_name="Вы продавец?")
	address = models.CharField(max_length=255, blank=True, verbose_name="Адрес")

	def get_absolute_url(self):
		return reverse("profile", args=[str(self.id)])
