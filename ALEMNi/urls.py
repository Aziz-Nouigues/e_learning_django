from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from authentification.views import home_view

urlpatterns = [
    path('', home_view, name='home'),
    path("admin/", admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("student_portal/", include("student_portal.urls")),
    path("tutor_portal/", include("tutor_portal.urls")),
    path("administrator_dash", include("administrator_dash.urls")),
    path("API_module", include("API_module.urls")),
    path("analytics", include("analytics.urls")),
    path("course_management", include("course_management.urls")),
    path("authentification/", include("authentification.urls")),
    path("frontend", include("frontend.urls")),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
