from django.urls import path
from .views import SignUpView, ProfilePage, UpdateProfile


urlpatterns = [
	path("signup/", SignUpView.as_view(), name="signup"),
	path("<int:pk>/", ProfilePage.as_view(), name="profile"),
	path("<int:pk>/update", UpdateProfile.as_view(), name="update_profile"),
]
