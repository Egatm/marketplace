from django.urls import path

from .views import HomePageView, news


urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("news/", news, name="news")
]
