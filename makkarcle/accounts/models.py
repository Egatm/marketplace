from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
	birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
	email = models.EmailField(max_length=255, unique=True, verbose_name="Адрес электронной почты")
	is_seller = models.BooleanField(default=False, verbose_name="Вы продавец?")

