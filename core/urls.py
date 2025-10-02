from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.urls import include, path

from .schema import swagger_urlpatterns

from apps.common.homepage import home


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("api/common/", include("apps.common.urls", namespace="common")),
    path("api/users/", include("apps.users.urls", namespace="users")),
    path("api/applications/", include("apps.applications.urls", namespace="applications")),

]

urlpatterns += swagger_urlpatterns

if not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
