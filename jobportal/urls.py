from django.contrib import admin


from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    #
    #
    # Versioned APIs
    path("api/<str:version>/auth/", include("accounts.urls")),
    path("api/<str:version>/company/", include("company.urls")),
    #
    #
    #
    # Schema and Swagger
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
