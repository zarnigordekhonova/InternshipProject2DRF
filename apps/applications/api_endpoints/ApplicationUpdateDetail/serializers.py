from rest_framework import serializers
from apps.applications.models import (Application, ApplicationBranch, 
                                      SpecialistsRequired, EquipmentRequired,
                                      EquipmentRequiredItem) 



class ApplicationBranchRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for retrieving branch data"""
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
            'branch',
            'branch_name',
            'district_name',
            'region_name',
            # 'specialties',
            'specialties_details',
            # 'selected_specialists',
            'selected_specialists_details',
            # 'selected_equipment',
            'selected_equipment_details'
        ]
    
    def get_specialties_details(self, obj):
        """Return list of specialty names"""
        return [{'id': s.id, 'name': s.name} for s in obj.specialties.all()]
    
    def get_selected_specialists_details(self, obj):
        """Return list of specialist details with min_count requirement"""
        specialists_data = []
        
        for sp in obj.selected_specialists.all():
            specialist_info = {
                'id': sp.id,
                'title': sp.title
            }
            
            # Find minimum required count for this specialist across selected specialties
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
        """Return list of equipment details with min_count requirement"""
        equipment_data = []
        
        for eq in obj.selected_equipment.all():
            equipment_info = {
                'id': eq.id,
                'name': eq.name
            }
            
            # Find minimum required count for this equipment across selected specialties
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
    """Serializer for retrieving application with branches"""
    branches = ApplicationBranchRetrieveSerializer(source='applicationbranch_set', many=True, read_only=True)
    
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