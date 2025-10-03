from django.urls import path

from apps.applications.api_endpoints import (
    # Branch
    BranchCreateAPIView,
    BranchListAPIView,
    BranchDetailUpdateAPIView,
    BranchDeleteAPIView,

    # Application
    ApplicationCreateAPIView,
    ApplicationListAPIView,
    ApplicationDetailUpdateAPIView,

    # Specialty
    SpecialtyCreateAPIView,
    SpecialtyListAPIView,
    SpecialtyUpdateDetailAPIView
)

app_name = "applications"

urlpatterns = [
    # Branch
    path("branch-create/", BranchCreateAPIView.as_view(), name="branch-create"),
    path("branch-list/", BranchListAPIView.as_view(), name="branch-list"),
    path("update/<int:pk>/branch/", BranchDetailUpdateAPIView.as_view(), name="branch-update-detail"),
    path("delete/<int:pk>/branch/", BranchDeleteAPIView.as_view(), name="branch-delete"),

    # Application
    path("application-create/", ApplicationCreateAPIView.as_view(), name="application-create"),
    path("application-list/", ApplicationListAPIView.as_view(), name="application-list"),
    path("application/<int:pk>/update/", ApplicationDetailUpdateAPIView.as_view(), name="application-update-detail"),

    # Specialty
    path("specialty-create/", SpecialtyCreateAPIView.as_view(), name="specialty-create"),
    path("specialty-list/", SpecialtyListAPIView.as_view(), name="specialty-list"),
    path("update/<int:pk>/specialty/", SpecialtyUpdateDetailAPIView.as_view(), name="specialty-update-detail"),

]