from django.urls import path, include
from rest_framework.routers import DefaultRouter
from company.views import JobView

router = DefaultRouter()
router.register(r"jobs", JobView, basename="jobs")

urlpatterns = [
    path("", include(router.urls)),
]
