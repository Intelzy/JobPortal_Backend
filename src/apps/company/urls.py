from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobView, ApplicantView, ProfileView


urlpatterns = [
    path("jobs/", JobView.as_view()),
    path("jobs/<int:id>/", JobView.as_view()),
    #
    path("applicants/", ApplicantView.as_view()),
    path("applicants/<int:id>/", ApplicantView.as_view()),
    #
    path("profile/<int:company_id>/", ProfileView.as_view()),
]
