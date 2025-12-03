from django.urls import path, include
from rest_framework.routers import DefaultRouter
from company.views import JobView, ApplicantView


urlpatterns = [
    path("applicants/", ApplicantView.as_view()),
    path("applicants/<int:id>/", ApplicantView.as_view()),
    path("applicants/<str:status>/", ApplicantView.as_view()),
    path("jobs/", JobView.as_view()),
    path("jobs/<int:id>/", JobView.as_view()),
]
