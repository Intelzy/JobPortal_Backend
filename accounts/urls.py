from django.urls import path

from accounts.views import UserView, LoginView

urlpatterns = [
    path("users/", UserView.as_view()),
    path("users/<int:id>/", UserView.as_view()),
    path("login/", LoginView.as_view()),
]
