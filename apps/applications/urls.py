from django.urls import path

from apps.applications.api_endpoints import (
    BranchCreateAPIView,
    BranchListAPIView,
    BranchUpdateAPIView,
    BranchDeleteAPIView
)

app_name = "applications"

urlpatterns = [
    path("branch-create/", BranchCreateAPIView.as_view(), name="branch-create"),
    path("branch-list/", BranchListAPIView.as_view(), name="branch-list"),
    path("update/<int:pk>/branch/", BranchUpdateAPIView.as_view(), name="branch-update"),
    path("delete/<int:pk>/branch/", BranchDeleteAPIView.as_view(), name="branch-delete")
]