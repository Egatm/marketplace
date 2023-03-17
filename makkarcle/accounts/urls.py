from django.urls import path
from .views import SignUpView, ProfilePage


urlpatterns = [
	path("signup/", SignUpView.as_view(), name="signup"),
	path("<int:pk>/", ProfilePage.as_view(), name="profile"),
]
