from django.urls import path

from .views import UserView, LoginView

urlpatterns = [
    path("users/", UserView.as_view()),
    path("users/<int:id>/", UserView.as_view()),
    path("login/", LoginView.as_view()),
]
