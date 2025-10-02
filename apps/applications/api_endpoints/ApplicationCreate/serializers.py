from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError as DjangoValidationError 

from rest_framework import serializers
from rest_framework.exceptions import ValidationError as DRFValidationError 

from apps.applications.models import Application, ApplicationBranch
    

class ApplicationBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationBranch
        fields = [
            'id',
            'branch',
            'specialties',
            'selected_specialists',
            'selected_equipment'
        ]

        extra_kwargs = {
            'specialties': {'allow_empty': False, 'required': True}, # Bu sizning required=True logikangiz
            'selected_specialists': {'required': False}, # nega required False => tekshirish kerak
            'selected_equipment': {'required': False},
        }

    def validate(self, data):
        
        specialties = data.get('specialties')
        selected_specialists = data.get('selected_specialists')
        selected_equipment = data.get('selected_equipment')
        
        if not specialties:
            raise DRFValidationError({
                'specialties': _("Iltimos, filial uchun ixtisoslik turlarini tanlang.")
            }, code='missing_specialties')

        # Mutaxassis talablarini tekshirish
        if specialties and selected_specialists:
            try:
                self._validate_specialist_requirements(specialties, selected_specialists)
            except DjangoValidationError as e:
                raise DRFValidationError({'selected_specialists': e.message})
                
        # Uskuna talablarini tekshirish
        if specialties and selected_equipment:
            try:
                self._validate_equipment_requirements(specialties, selected_equipment)
            except DjangoValidationError as e:
                raise DRFValidationError({'selected_equipment': e.message})

        return data

    # Formadagi _validate_specialist_requirements metodining o'xshashi
    def _validate_specialist_requirements(self, specialties_qs, selected_specialists_qs):
        from apps.applications.models import SpecialistsRequired 

        errors = []
        
        for specialty in specialties_qs:
            required_qs = SpecialistsRequired.objects.filter(specialty=specialty)
            
            for requirement in required_qs:
                required_title = requirement.required_specialists.title
                min_count = requirement.min_count
                
                selected_count = 0
                for specialist in selected_specialists_qs:
                    if hasattr(specialist, 'title') and specialist.title == required_title:
                         selected_count += 1
                
                if selected_count < min_count:
                    errors.append(
                        f'"{specialty.name}" ixtisosligi uchun "{required_title}" lavozimidan '
                        f'kamida {min_count} ta tanlash shart (Siz {selected_count} ta tanladingiz).'
                    )
        
        if errors:
            error_message = "Minimal talab qilinadigan mutaxassislarni to'liq tanlamadingiz:\n" + "\n".join(f"• {err}" for err in errors)
            raise DjangoValidationError(error_message, code='insufficient_specialists')


    def _validate_equipment_requirements(self, specialties_qs, selected_equipment_qs):
        from apps.applications.models import EquipmentRequired, EquipmentRequiredItem # importni shu yerga olib o'tish

        for specialty in specialties_qs:
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
                
                selected_count = 0
                for equipment in selected_equipment_qs:
                    if hasattr(equipment, 'name') and equipment.name == equipment_name:
                         selected_count += 1
                
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
                
class ApplicationBranchListSerializer(serializers.ListSerializer):
    """
    Bu ListSerializer Application modellarini yaratish/yangilash uchun
    ApplicationBranch ob'ektlari ro'yxatini boshqaradi.
    """
    child = ApplicationBranchSerializer()
    

class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        branches = ApplicationBranchListSerializer(many=True)
        model = Application
        fields = [
            'first_name', 'last_name', 'paternal_name', 'phone_number', 
            'email', 'document_type', 'document_file', 'full_address'
        ]
        
    def clean_document_file(self):
        document_file = self.cleaned_data.get('document_file')
        
        if document_file:
            MAX_FILE_SIZE = 10 * 1024 * 1024 
            if document_file.size > MAX_FILE_SIZE:
                raise serializers.ValidationError(_("Fayl hajmi 10 MB dan oshmasligi kerak."))
                
            file_extension = document_file.name.split('.')[-1].lower()
            ALLOWED_EXTENSIONS = ['pdf', 'jpg', 'png']
            
            if file_extension not in ALLOWED_EXTENSIONS:
                raise serializers.ValidationError(_("Faqat PDF, JPG va PNG formatlari ruxsat etiladi."))
                
        return document_file