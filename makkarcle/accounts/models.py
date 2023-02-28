from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
	birth_date = models.DateField(null=True, blank=True)
	email = models.EmailField(max_length=255, unique=True)
	is_seller = models.BooleanField(default=False)
	# email_verify = models.BooleanField(default=False)
