from rest_framework import serializers
from django.utils.translation import gettext as _

from apps.applications.models import (
    Application, ApplicationBranch, Specialty, 
    Specialist, Equipment, SpecialistsRequired,
    EquipmentRequired, EquipmentRequiredItem, Branch
)


class ApplicationBranchSerializer(serializers.Serializer):
    branch = serializers.CharField()

    specialties = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False
    )
    selected_specialists = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True
    )
    selected_equipment = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True
    )

    def validate_branch(self, value):
        try:
            branch = Branch.objects.get(branch_name__iexact=value.strip())
            return branch
        except Branch.DoesNotExist:
            raise serializers.ValidationError(
               f'Filial "{value}" topilmadi. Iltimos, to\'g\'ri filial nomini kiriting.'
            )
        except Branch.MultipleObjectsReturned:
            raise serializers.ValidationError(
                f'"{value}" nomli bir nechta filial mavjud. Aniqroq nom kiriting.'
            )

    def validate_specialties(self, value):
        specialty_objects = []
        not_found = []
        
        for specialty_name in value:
            try:
                specialty = Specialty.objects.get(name__iexact=specialty_name.strip())
                specialty_objects.append(specialty)
            except Specialty.DoesNotExist:
                not_found.append(specialty_name)
            except Specialty.MultipleObjectsReturned:
                raise serializers.ValidationError(
                   f'"{specialty_name}" nomli bir nechta ixtisoslik mavjud. Aniqroq nom kiriting.'
                )
        
        if not_found:
            raise serializers.ValidationError(
                f'Quyidagi ixtisosliklar topilmadi: {", ".join(not_found)}'
            )
        
        return specialty_objects

    def validate_selected_specialists(self, value):
        if not value:
            return []
        
        specialist_objects = []
        not_found = []
        
        for specialist_title in value:
            try:
                specialist = Specialist.objects.get(title__iexact=specialist_title.strip())
                specialist_objects.append(specialist)
            except Specialist.DoesNotExist:
                not_found.append(specialist_title)
            except Specialist.MultipleObjectsReturned:
                raise serializers.ValidationError(
                    f'"{specialist_title}" lavozimli bir nechta mutaxassis mavjud. Aniqroq lavozim kiriting.'
                )
        
        if not_found:
            raise serializers.ValidationError(
                f'Quyidagi mutaxassislar topilmadi: {", ".join(not_found)}'
            )
        
        return specialist_objects

    def validate_selected_equipment(self, value):
        if not value:
            return []
        
        equipment_objects = []
        not_found = []
        
        for equipment_name in value:
            try:
                equipment = Equipment.objects.get(name__iexact=equipment_name.strip())
                equipment_objects.append(equipment)
            except Equipment.DoesNotExist:
                not_found.append(equipment_name)
            except Equipment.MultipleObjectsReturned:
                raise serializers.ValidationError(
                   f'"{equipment_name}" nomli bir nechta uskuna mavjud. Aniqroq nom kiriting.'
                )
        
        if not_found:
            raise serializers.ValidationError(
                f'Quyidagi uskunalar topilmadi: {", ".join(not_found)}'
            )
        
        return equipment_objects

    def validate(self, data):
        specialties = data.get('specialties', [])
        selected_specialists = data.get('selected_specialists', [])
        selected_equipment = data.get('selected_equipment', [])
        
        specialist_requirements = self._get_specialist_requirements(specialties)
        equipment_requirements = self._get_equipment_requirements(specialties)
        
        specialist_errors = self._validate_specialist_requirements(
            specialties,
            selected_specialists,
            specialist_requirements
        )
        
        equipment_errors = self._validate_equipment_requirements(
            specialties,
            selected_equipment,
            equipment_requirements
        )
        
        if specialist_errors or equipment_errors:
            error_details = {
                'requirements_not_met': True,
                'specialist_requirements': specialist_requirements,
                'equipment_requirements': equipment_requirements,
            }
            
            if specialist_errors:
                error_details['specialist_errors'] = specialist_errors
            if equipment_errors:
                error_details['equipment_errors'] = equipment_errors
            
            raise serializers.ValidationError(error_details)
        
        return data

    def _get_specialist_requirements(self, specialties):
        requirements = []
        
        for specialty in specialties:
            required_qs = SpecialistsRequired.objects.filter(
                specialty=specialty
            ).select_related('required_specialists')
            
            for req in required_qs:
                requirements.append({
                    'specialty': specialty.name,
                    'specialist_title': req.required_specialists.title,
                    'min_count': req.min_count
                })
        
        return requirements

    def _get_equipment_requirements(self, specialties):
        requirements = []
        
        for specialty in specialties:
            try:
                equipment_req = EquipmentRequired.objects.get(specialty=specialty)
                items = EquipmentRequiredItem.objects.filter(
                    equipment_required=equipment_req
                ).select_related('equipment')
                
                for item in items:
                    requirements.append({
                        'specialty': specialty.name,
                        'equipment_name': item.equipment.name,
                        'min_count': item.min_count
                    })
            except EquipmentRequired.DoesNotExist:
                continue
        
        return requirements

    def _validate_specialist_requirements(self, specialties, selected_specialists, requirements):
        errors = []
        
        for req in requirements:
            count = sum(1 for sp in selected_specialists if sp.title == req['specialist_title'])
            
            if count < req['min_count']:
                errors.append({
                    'specialty': req['specialty'],
                    'specialist_title': req['specialist_title'],
                    'required': req['min_count'],
                    'provided': count,
                    'message': (
                        f'"{req["specialty"]}" ixtisosligi uchun "{req["specialist_title"]}" '
                        f'lavozimidan kamida {req["min_count"]} ta kerak '
                        f'(Siz {count} ta tanladingiz)'
                    )
                })
        
        return errors

    def _validate_equipment_requirements(self, specialties, selected_equipment, requirements):
        errors = []
        
        for req in requirements:
            count = sum(1 for eq in selected_equipment if eq.name == req['equipment_name'])
            
            if count < req['min_count']:
                errors.append({
                    'specialty': req['specialty'],
                    'equipment_name': req['equipment_name'],
                    'required': req['min_count'],
                    'provided': count,
                    'message': (
                        f'"{req["specialty"]}" ixtisosligi uchun "{req["equipment_name"]}" '
                        f'dan kamida {req["min_count"]} ta kerak '
                        f'(Siz {count} ta tanladingiz)'
                    )
                })
        
        return errors


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