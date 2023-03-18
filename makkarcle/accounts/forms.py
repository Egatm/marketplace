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


# class UserUpdateForm(UserCreationForm):
# 	class Meta:
# 		model = CustomUser
# 		fields = ['username', 'email', 'first_name', 'last_name', 'birth_date']