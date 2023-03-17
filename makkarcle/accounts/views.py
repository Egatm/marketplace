from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.views import View

from .forms import CustomUserCreationForm
from .models import CustomUser


# Create your views here.
class SignUpView(CreateView):
	form_class = CustomUserCreationForm
	success_url = reverse_lazy('login')
	template_name = "registration/signup.html"


class ProfilePage(DetailView):
	model = CustomUser
	template_name = "accounts/profile_page.html"


class UpdateProfile(UpdateView):
	model = CustomUser
	fields = (
		"username",
		"email",
		"birth_date",
		"firstname",
		"lastname",
	)
	template_name = "accounts/profile_edit.html"