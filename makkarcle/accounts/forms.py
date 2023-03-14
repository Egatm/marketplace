from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
	class Meta(UserCreationForm):
		model = CustomUser
		fields = ("username", "email", "is_seller")


class CustomUserChangeForm(UserChangeForm):
	class Meta:
		model = CustomUser
		fields = ("username", "email", "is_seller")
