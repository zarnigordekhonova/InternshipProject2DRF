from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from apps.applications.models import (
    Region, District, Branch, Specialty, Specialist,
    SpecialistsRequired, Equipment, EquipmentRequired,
    EquipmentRequiredItem, Application, ApplicationBranch
)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'region_name',)
    search_fields = ('region_name',)
    ordering = ('region_name',)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'district_name', 'region')
    list_filter = ('region',)
    search_fields = ('district_name', 'region__region_name')
    autocomplete_fields = ['region']
    ordering = ('region', 'district_name')


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'branch_name', 'district', 'get_region')
    list_filter = ('district__region', 'district')
    search_fields = ('branch_name', 'district__district_name', 'district__region__region_name')
    autocomplete_fields = ['district']
    ordering = ('district__region', 'district', 'branch_name')
    
    def get_region(self, obj):
        return obj.district.region.region_name
    get_region.short_description = _('Region')
    get_region.admin_order_field = 'district__region__region_name'


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    search_fields = ('title',)
    ordering = ('title',)


@admin.register(SpecialistsRequired)
class SpecialistsRequiredAdmin(admin.ModelAdmin):
    list_display = ('id', 'specialty', 'required_specialists', 'min_count')
    list_filter = ('specialty', 'required_specialists')
    search_fields = ('specialty__name', 'required_specialists__title')
    autocomplete_fields = ['specialty', 'required_specialists']
    ordering = ('specialty', 'required_specialists')
    
    fieldsets = (
        (_('Specialty Information'), {
            'fields': ('specialty',)
        }),
        (_('Requirements'), {
            'fields': ('required_specialists', 'min_count')
        }),
    )


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description_short')
    search_fields = ('name', 'description')
    ordering = ('name',)
    
    fieldsets = (
        (_('Equipment Information'), {
            'fields': ('name', 'description')
        }),
    )
    
    def description_short(self, obj):
        if obj.description:
            return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
        return '-'
    description_short.short_description = _('Description')


class EquipmentRequiredItemInline(admin.TabularInline):
    model = EquipmentRequiredItem
    extra = 1
    autocomplete_fields = ['equipment']
    fields = ('equipment', 'min_count')


@admin.register(EquipmentRequired)
class EquipmentRequiredAdmin(admin.ModelAdmin):
    list_display = ('id', 'specialty', 'get_equipment_count')
    search_fields = ('specialty__name',)
    autocomplete_fields = ['specialty']
    inlines = [EquipmentRequiredItemInline]
    ordering = ('specialty',)
    
    def get_equipment_count(self, obj):
        return obj.items.count()
    get_equipment_count.short_description = _('Equipment Count')


class ApplicationBranchInline(admin.TabularInline):
    model = ApplicationBranch
    extra = 1
    autocomplete_fields = ['branch']
    filter_horizontal = ('specialties', 'selected_specialists', 'selected_equipment')
    verbose_name = _("Branch")
    verbose_name_plural = _("Branches")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'registration_number', 
        'full_name', 
        'email', 
        'phone_number', 
        'status', 
        'created_at'
    )
    list_filter = ('status', 'created_at', 'updated_at', 'document_type')
    search_fields = (
        'registration_number', 
        'first_name', 
        'last_name', 
        'email', 
        'phone_number',
        'user__username'
    )
    readonly_fields = ('created_at', 'updated_at', 'registration_number')
    autocomplete_fields = ['user']
    date_hierarchy = 'created_at'
    inlines = [ApplicationBranchInline]
    
    fieldsets = (
        (_('User Information'), {
            'fields': ('user',)
        }),
        (_('Personal Information'), {
            'fields': ('first_name', 'last_name', 'paternal_name', 'full_address')
        }),
        (_('Contact Information'), {
            'fields': ('phone_number', 'email')
        }),
        (_('Documents'), {
            'fields': ('document_type', 'document_file', 'registration_number')
        }),
        (_('Status & Timestamps'), {
            'fields': ('status', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = _('Full Name')
    full_name.admin_order_field = 'first_name'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user')


@admin.register(ApplicationBranch)
class ApplicationBranchAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'application', 
        'branch', 
        'get_district', 
        'get_specialties_count',
        'get_specialists_count',
        'get_equipment_count'
    )
    list_filter = (
        'branch__district__region',
        'branch__district',
        'specialties'
    )
    search_fields = (
        'application__registration_number',
        'application__first_name',
        'application__last_name',
        'branch__branch_name',
        'branch__district__district_name'
    )
    autocomplete_fields = ['application', 'branch']
    filter_horizontal = ('specialties', 'selected_specialists', 'selected_equipment')
    
    fieldsets = (
        (_('Application & Branch'), {
            'fields': ('application', 'branch')
        }),
        (_('Specialties'), {
            'fields': ('specialties',)
        }),
        (_('Selected Specialists'), {
            'fields': ('selected_specialists',)
        }),
        (_('Selected Equipment'), {
            'fields': ('selected_equipment',)
        }),
    )
    
    def get_district(self, obj):
        return obj.branch.district.district_name
    get_district.short_description = _('District')
    get_district.admin_order_field = 'branch__district__district_name'
    
    def get_specialties_count(self, obj):
        return obj.specialties.count()
    get_specialties_count.short_description = _('Specialties')
    
    def get_specialists_count(self, obj):
        return obj.selected_specialists.count()
    get_specialists_count.short_description = _('Specialists')
    
    def get_equipment_count(self, obj):
        return obj.selected_equipment.count()
    get_equipment_count.short_description = _('Equipment')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            'application',
            'branch',
            'branch__district',
            'branch__district__region'
        ).prefetch_related(
            'specialties',
            'selected_specialists',
            'selected_equipment'
        )