from django.contrib import admin


from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    # Versioned APIs
    path("api/<str:version>/auth/", include("src.apps.accounts.urls")),
    path("api/<str:version>/company/", include("src.apps.company.urls")),
    # Schema and Swagger
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
