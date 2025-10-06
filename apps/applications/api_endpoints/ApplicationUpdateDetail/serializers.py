from django.utils.translation import gettext as _

from rest_framework import serializers

from apps.applications.models import (Application, ApplicationBranch, 
                                      SpecialistsRequired, EquipmentRequired,
                                      EquipmentRequiredItem) 
from apps.applications.api_endpoints.ApplicationCreate.serializers import ApplicationBranchSerializer


class ApplicationUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating applications with string inputs and allows partial updates.
    """
    branches = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False,
        allow_empty=False
    )
    
    class Meta:
        model = Application
        fields = [
            'first_name', 'last_name', 'paternal_name', 'phone_number', 
            'email', 'document_type', 'document_file', 'full_address', 'branches'
        ]
    
    def validate_branches(self, value):
        """Validate branches data using string inputs"""
        if not isinstance(value, list):
            raise serializers.ValidationError(_("Branches must be a list"))
        
        if len(value) == 0:
            raise serializers.ValidationError(_("At least one branch is required"))
        
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
                raise serializers.ValidationError(
                    _("Fayl hajmi 10 MB dan oshmasligi kerak.")
                )
                
            file_extension = document_file.name.split('.')[-1].lower()
            ALLOWED_EXTENSIONS = ['pdf', 'jpg', 'png']
            
            if file_extension not in ALLOWED_EXTENSIONS:
                raise serializers.ValidationError(
                    _("Faqat PDF, JPG va PNG formatlari ruxsat etiladi.")
                )
                
        return document_file
    
    def update(self, instance, validated_data):
        branches_data = validated_data.pop('branches', None)
        
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        
        if branches_data is not None:
            for branch_data in branches_data:
                specialties = branch_data.pop('specialties', [])
                selected_specialists = branch_data.pop('selected_specialists', [])
                selected_equipment = branch_data.pop('selected_equipment', [])
                branch_instance = branch_data.pop('branch')
                
                app_branch = ApplicationBranch.objects.create(
                    application=instance,
                    branch=branch_instance
                )
                
                if specialties:
                    app_branch.specialties.set(specialties)
                if selected_specialists:
                    app_branch.selected_specialists.set(selected_specialists)
                if selected_equipment:
                    app_branch.selected_equipment.set(selected_equipment)
        
        return instance
                                      

class ApplicationBranchRetrieveSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.branch_name', read_only=True)
    district_name = serializers.CharField(source='branch.district.district_name', read_only=True)
    region_name = serializers.CharField(source='branch.district.region.region_name', read_only=True)
    
    specialties_details = serializers.SerializerMethodField()
    selected_specialists_details = serializers.SerializerMethodField()
    selected_equipment_details = serializers.SerializerMethodField()
    
    class Meta:
        model = ApplicationBranch
        fields = [
            'id',
            'branch_name',
            'district_name',
            'region_name',
            'specialties_details',
            'selected_specialists_details',
            'selected_equipment_details'
        ]
    
    def get_specialties_details(self, obj):
        return [{'id': s.id, 'name': s.name} for s in obj.specialties.all()]
    
    def get_selected_specialists_details(self, obj):
        specialists_data = []
        
        for sp in obj.selected_specialists.all():
            specialist_info = {'id': sp.id, 'title': sp.title}
            
            min_requirements = []
            for specialty in obj.specialties.all():
                try:
                    requirement = SpecialistsRequired.objects.get(
                        specialty=specialty,
                        required_specialists=sp
                    )
                    min_requirements.append({
                        'specialty_name': specialty.name,
                        'min_count': requirement.min_count
                    })
                except SpecialistsRequired.DoesNotExist:
                    continue
            
            if min_requirements:
                specialist_info['requirements'] = min_requirements
            
            specialists_data.append(specialist_info)
        
        return specialists_data
    
    def get_selected_equipment_details(self, obj):
        equipment_data = []
        
        for eq in obj.selected_equipment.all():
            equipment_info = {'id': eq.id, 'name': eq.name}
            
            min_requirements = []
            for specialty in obj.specialties.all():
                try:
                    equipment_req = EquipmentRequired.objects.get(specialty=specialty)
                    equipment_item = EquipmentRequiredItem.objects.get(
                        equipment_required=equipment_req,
                        equipment=eq
                    )
                    min_requirements.append({
                        'specialty_name': specialty.name,
                        'min_count': equipment_item.min_count
                    })
                except (EquipmentRequired.DoesNotExist, EquipmentRequiredItem.DoesNotExist):
                    continue
            
            if min_requirements:
                equipment_info['requirements'] = min_requirements
            
            equipment_data.append(equipment_info)
        
        return equipment_data


class ApplicationRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for retrieving application with branch information"""
    branches = ApplicationBranchRetrieveSerializer(
        source='applicationbranch_set',
        many=True,
        read_only=True
    )
    
    class Meta:
        model = Application
        fields = [
            'id',
            'first_name',
            'last_name',
            'paternal_name',
            'phone_number',
            'email',
            'document_type',
            'document_file',
            'full_address',
            'registration_number',
            'status',
            'created_at',
            'updated_at',
            'branches'
        ]