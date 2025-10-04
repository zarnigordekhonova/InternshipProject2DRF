from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from apps.applications.models import Application
from apps.applications.choices import ApplicationStatus
from apps.applications.utils import generate_registration_number, send_application_email
from apps.applications.api_endpoints.ApplicationUpdateDetail.serializers import ApplicationUpdateSerializer
from apps.applications.api_endpoints.ApplicationUpdateDetail.serializers import ApplicationRetrieveSerializer


class ApplicationDetailUpdateAPIView(RetrieveUpdateAPIView):
    """
    Updating/Getting information of application on special ID.

    PUT /api/applications/application/{id}/update/
    PATCH /api/applications/application/{id}/update/
    Update an existing application

    GET /api/applications/application/{id}/update/
    To get an application data in detail on specific ID
    
    Supports 'action' parameter:
    - 'save': Keep as DRAFT
    - 'submit': Change to SUBMITTED (generates registration number and sends email)
    """
    serializer_class = ApplicationUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    
    def get_queryset(self):
        queryset = Application.objects.select_related('user').prefetch_related(
            'applicationbranch_set__branch__district__region',
            'applicationbranch_set__specialties',
            'applicationbranch_set__selected_specialists',
            'applicationbranch_set__selected_equipment'
        )
        
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        
        return queryset
    
    def get_serializer_class(self):
        """Use different serializer for GET and PUT/PATCH"""
        if self.request.method == 'GET':
            return ApplicationRetrieveSerializer
        return ApplicationUpdateSerializer
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        action = request.data.get('action', 'save').lower()
        
        if action not in ['submit', 'save']:
            return Response({
                'success': False,
                'message': _("Noto'g'ri harakat turi. 'submit' yoki 'save' bo'lishi kerak.")
            }, status=status.HTTP_400_BAD_REQUEST)
        
    
        if instance.status != ApplicationStatus.DRAFT:
            return Response({
                'success': False,
                'message': _("Faqat 'DRAFT' statusidagi arizalarni tahrirlash mumkin.")
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        try:
            serializer.is_valid(raise_exception=True)
            
            if 'branches' in request.data:
                instance.applicationbranch_set.all().delete()
            
            application = serializer.save()
            
            if action == ApplicationStatus.SUBMITTED:
                if not application.registration_number:
                    registration_number = generate_registration_number()
                    application.registration_number = registration_number
                
                # Update status to SUBMITTED
                application.status = ApplicationStatus.SUBMITTED
                application.save(update_fields=['status', 'registration_number'])
                
                # Send email notification if status is SUBMITTED
                try:
                    send_application_email(application)
                except Exception as e:
                    print(f"Email sending failed: {str(e)}")
                
                message = _("Ariza muvaffaqiyatli yuborildi! Ro'yxatdan o'tish raqamingiz: {reg_number}").format(
                    reg_number=application.registration_number
                )
            else:
                message = _("Ariza qoralama sifatida saqlandi.")
            
            return Response({
                'success': True,
                'message': message,
                'data': {
                    'id': application.id,
                    'registration_number': application.registration_number,
                    'status': application.status,
                    'action': action,
                }
            }, status=status.HTTP_200_OK)
            
        except ValidationError as e:
            return Response({
                'success': False,
                'message': _("Ariza yangilashda xatolik yuz berdi."),
                'errors': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'message': _("Kutilmagan xatolik yuz berdi."),
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

__all__ = [
    'ApplicationDetailUpdateAPIView'
]