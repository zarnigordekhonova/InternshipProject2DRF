from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError as DjangoValidationError 
from rest_framework import serializers
from rest_framework.exceptions import ValidationError as DRFValidationError 
import json

from apps.applications.models import (
    Application, ApplicationBranch, Specialty, 
    Specialist, Equipment, SpecialistsRequired,
    EquipmentRequired, EquipmentRequiredItem
)


class ApplicationBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationBranch
        fields = [
            'branch',
            'specialties',
            'selected_specialists',
            'selected_equipment'
        ]
        extra_kwargs = {
            'specialties': {'allow_empty': False, 'required': True}, 
            'selected_specialists': {'required': False},
            'selected_equipment': {'required': False},
        }

    def validate(self, data):
        specialties = data.get('specialties')
        selected_specialists = data.get('selected_specialists', [])
        selected_equipment = data.get('selected_equipment', [])
        
        if not specialties:
            raise DRFValidationError({
                'specialties': _("Iltimos, filial uchun ixtisoslik turlarini tanlang.")
            }, code='missing_specialties')

        # At this point, DRF has already converted IDs to model instances
        # Extract IDs for validation
        specialty_ids = [s.id if hasattr(s, 'id') else s for s in specialties]
        specialist_ids = [sp.id if hasattr(sp, 'id') else sp for sp in selected_specialists]
        equipment_ids = [eq.id if hasattr(eq, 'id') else eq for eq in selected_equipment]

        # Validate specialist requirements
        if specialty_ids and specialist_ids:
            try:
                self._validate_specialist_requirements(specialty_ids, specialist_ids)
            except DjangoValidationError as e:
                raise DRFValidationError({'selected_specialists': str(e.message)})
                
        # Validate equipment requirements
        if specialty_ids and equipment_ids:
            try:
                self._validate_equipment_requirements(specialty_ids, equipment_ids)
            except DjangoValidationError as e:
                raise DRFValidationError({'selected_equipment': str(e.message)})

        return data

    def _validate_specialist_requirements(self, specialties_list, selected_specialists_list):
        """
        Validate that selected specialists meet minimum requirements
        specialties_list: list of Specialty IDs
        selected_specialists_list: list of Specialist IDs
        """
        errors = []
        
        # Get specialty objects
        specialties = Specialty.objects.filter(id__in=specialties_list)
        
        # Get selected specialist objects
        selected_specialists = Specialist.objects.filter(id__in=selected_specialists_list)
        
        for specialty in specialties:
            required_qs = SpecialistsRequired.objects.filter(
                specialty=specialty
            ).select_related('required_specialists')
            
            for requirement in required_qs:
                required_title = requirement.required_specialists.title
                min_count = requirement.min_count
                
                # Count how many of this type were selected
                selected_count = selected_specialists.filter(title=required_title).count()
                
                if selected_count < min_count:
                    errors.append(
                        f'"{specialty.name}" ixtisosligi uchun "{required_title}" lavozimidan '
                        f'kamida {min_count} ta tanlash shart (Siz {selected_count} ta tanladingiz).'
                    )
        
        if errors:
            error_message = "Minimal talab qilinadigan mutaxassislarni to'liq tanlamadingiz:\n" + "\n".join(f"• {err}" for err in errors)
            raise DjangoValidationError(error_message, code='insufficient_specialists')

    def _validate_equipment_requirements(self, specialties_list, selected_equipment_list):
        """
        Validate that selected equipment meets minimum requirements
        specialties_list: list of Specialty IDs
        selected_equipment_list: list of Equipment IDs
        """
        specialties = Specialty.objects.filter(id__in=specialties_list)
        
        selected_equipment = Equipment.objects.filter(id__in=selected_equipment_list)
        
        for specialty in specialties:
            try:
                equipment_req = EquipmentRequired.objects.get(specialty=specialty)
            except EquipmentRequired.DoesNotExist:
                continue
            
            required_items = EquipmentRequiredItem.objects.filter(
                equipment_required=equipment_req
            ).select_related('equipment')
            
            for item in required_items:
                equipment_name = item.equipment.name
                min_count = item.min_count
                
                # Count how many of this type were selected
                selected_count = selected_equipment.filter(name=equipment_name).count()
                
                if selected_count < min_count:
                    raise DjangoValidationError(
                        _("%(specialty)s ixtisosligi uchun \"%(equipment)s\" dan kamida %(min_count)s ta kiritilishi shart (Kiritilgani: %(selected_count)s).") % {
                            'specialty': specialty.name,
                            'equipment': equipment_name,
                            'min_count': min_count,
                            'selected_count': selected_count
                        },
                        code='insufficient_equipment'
                    )


class ApplicationCreateSerializer(serializers.ModelSerializer):
    branches = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        allow_empty=False
    )
    
    class Meta:
        model = Application
        fields = [
            'first_name', 'last_name', 'paternal_name', 'phone_number', 
            'email', 'document_type', 'document_file', 'full_address', 'branches'
        ]
    
    def validate_branches(self, value):
        """
        Validate branches data
        """
        if not isinstance(value, list):
            raise serializers.ValidationError("Branches must be a list")
        
        if len(value) == 0:
            raise serializers.ValidationError("At least one branch is required")
        
        validated_branches = []
        errors = {}
        
        for idx, branch_data in enumerate(value):
            serializer = ApplicationBranchSerializer(data=branch_data)
            if serializer.is_valid():
                validated_branches.append(serializer.validated_data)
            else:
                errors[f"branch_{idx}"] = serializer.errors
        
        if errors:
            raise serializers.ValidationError(errors)
        
        return validated_branches
        
    def validate_document_file(self, document_file):
        if document_file:
            MAX_FILE_SIZE = 10 * 1024 * 1024 
            if document_file.size > MAX_FILE_SIZE:
                raise serializers.ValidationError(_("Fayl hajmi 10 MB dan oshmasligi kerak."))
                
            file_extension = document_file.name.split('.')[-1].lower()
            ALLOWED_EXTENSIONS = ['pdf', 'jpg', 'png']
            
            if file_extension not in ALLOWED_EXTENSIONS:
                raise serializers.ValidationError(_("Faqat PDF, JPG va PNG formatlari ruxsat etiladi."))
                
        return document_file
    
    def create(self, validated_data):
        branches_data = validated_data.pop('branches')
        
        application_instance = Application.objects.create(**validated_data)
        
        for branch_data in branches_data:
            specialties = branch_data.pop('specialties', [])
            selected_specialists = branch_data.pop('selected_specialists', [])
            selected_equipment = branch_data.pop('selected_equipment', [])
            
            branch_instance = branch_data.pop('branch')
            
            app_branch = ApplicationBranch.objects.create(
                application=application_instance,
                branch=branch_instance
            )
            
            if specialties:
                app_branch.specialties.set(specialties)
            if selected_specialists:
                app_branch.selected_specialists.set(selected_specialists)
            if selected_equipment:
                app_branch.selected_equipment.set(selected_equipment)
        
        return application_instance