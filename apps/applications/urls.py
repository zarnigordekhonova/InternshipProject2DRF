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
    SpecialtyUpdateDetailAPIView, 
    SpecialtyDeleteAPIView,

    # Specialist
    SpecialistCreateAPIView,
    SpecialistListAPIView,
    SpecialistUpdateDetailAPIView,
    SpecialistDeleteAPIView,

    # SpecialistRequired
    SpecialistsRequiredCreateAPIView,
    SpecialistsRequiredListAPIView,
    SpecialistRequiredDetailUpdateAPIView,
    SpecialistsRequiredDeleteAPIView,

    # Equipment
    EquipmentCreateAPIView,
    EquipmentListAPIView,
    EquipmentUpdateDetailAPIView,
    EquipmentDeleteAPIView,

    # EquipmentRequired
    EquipmentRequiredItemCreateAPIView,
    EquipmentRequiredItemListAPIView,
    EquipmentRequiredItemRetrieveUpdateAPIView,
    EquipmentRequiredItemDestroyAPIView,
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
    path("delete/<int:pk>/specialty/", SpecialtyDeleteAPIView.as_view(), name="specialty-delete"),

    # Specialist
    path("specialist-create/", SpecialistCreateAPIView.as_view(), name="specialist-create"),
    path("specialist-list/", SpecialistListAPIView.as_view(), name="specialist-list"),
    path("update/<int:pk>/specialist/", SpecialistUpdateDetailAPIView.as_view(), name="specialist-update-detail"),
    path("delete/<int:pk>/specialist/", SpecialistDeleteAPIView.as_view(), name="specialist-delete"),

    # SpecialistRequired
    path("specialist-required-create/", SpecialistsRequiredCreateAPIView.as_view(), name="specialist-required-create"),
    path("specialist-required-list/", SpecialistsRequiredListAPIView.as_view(), name="specialist-required-list"),
    path("update/<int:pk>/specialists-required/", SpecialistRequiredDetailUpdateAPIView.as_view(), name="specialist-required-update-detail"),
    path("delete/<int:pk>/specialists-required/", SpecialistsRequiredDeleteAPIView.as_view(), name="specialist-required-delete"),

    # Equipment
    path("equipment-create/", EquipmentCreateAPIView.as_view(), name="equipment-create"),
    path("equipment-list/", EquipmentListAPIView.as_view(), name="equipment-list"),
    path("update/<int:pk>/equipment/", EquipmentUpdateDetailAPIView.as_view(), name="equipment-update-detail"),
    path("delete/<int:pk>/equipment/", EquipmentDeleteAPIView.as_view(), name="equipment-delete"),

    # EquipmentRequired
    path("equipment-required-create/", EquipmentRequiredItemCreateAPIView.as_view(), name="equipment-required-create"),
    path("equipment-required-list/", EquipmentRequiredItemListAPIView.as_view(), name="equipment-required-list"),
    path("update/<int:pk>/equipment-required/", 
         EquipmentRequiredItemRetrieveUpdateAPIView.as_view(), 
         name="equipment-required-update-detail"),
    path("delete/<int:pk>/equipment-required/", EquipmentRequiredItemDestroyAPIView.as_view(), name="equipment-required-delete"),
]