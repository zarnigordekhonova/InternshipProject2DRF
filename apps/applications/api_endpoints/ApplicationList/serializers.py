from rest_framework import serializers

from apps.applications.models import Application


class ApplicationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing applications"""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Application
        fields = [
            'id','full_name', 'registration_number',
           'status', 'created_at'
        ]
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name} {obj.paternal_name}"