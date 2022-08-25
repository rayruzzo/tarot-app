from django.urls import path
from .views import pastPresentFuture, home

urlpatterns = [
    path("reading", pastPresentFuture, name="reading"),
    path("", home, name="home"),
]