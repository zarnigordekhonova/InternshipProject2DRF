from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from apps.applications.choices import ApplicationStatus
from apps.applications.utils import generate_registration_number, send_application_email
from apps.applications.api_endpoints.ApplicationCreate.serializers import ApplicationCreateSerializer


class ApplicationCreateAPIView(CreateAPIView):
    """
    POST /api/applications/create/
    Create a new application with branches
    
    Request body example:
    {
        "action": "submit",  // or "save" for draft
        "first_name": "John",
        "last_name": "Doe",
        "paternal_name": "Smith",
        "phone_number": "+998901234567",
        "email": "john@example.com",
        "document_type": "Passport",
        "document_file": <file>,
        "full_address": "123 Main St",
        "branches": [
            {
                "branch": 1,
                "specialties": [1, 2],
                "selected_specialists": [1, 2, 3],
                "selected_equipment": [1, 2]
            }
        ]
    }
    """
    serializer_class = ApplicationCreateSerializer
    permission_classes = [IsAuthenticated]  
    
    def perform_create(self, serializer, action):
        """
        Create application with appropriate status based on action
        """
        if action == 'submit':
            application_status = ApplicationStatus.SUBMITTED  
        else:
            application_status = ApplicationStatus.DRAFT
        
        if self.request.user.is_authenticated:
            application = serializer.save(
                user=self.request.user,
                status=application_status
            )
        else:
            application = serializer.save(status=application_status)
        
        if action == 'submit':
            registration_number = generate_registration_number()
            application.registration_number = registration_number
            application.save(update_fields=['registration_number'])
         
            try:
                send_application_email(application)
            except Exception as e:
                print(f"Email sending failed: {str(e)}")
        
        return application
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Handle application creation with submit/save logic
        """ 
        action = request.data.get('action', 'save').lower()
        
        if action not in ['submit', 'save']:
            return Response({
                'success': False,
                'message': _("Noto'g'ri harakat turi. 'submit' yoki 'save' bo'lishi kerak.")
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            application = self.perform_create(serializer, action)
            
            # Prepare response message based on action
            if action == 'submit':
                message = _("Ariza muvaffaqiyatli yuborildi! Ro'yxatdan o'tish raqamingiz: {reg_number}").format(
                    reg_number=application.registration_number
                )
            else:
                message = _("Ariza qoralama sifatida saqlandi. Keyinroq tahrirlashingiz mumkin.")
            
            return Response({
                'success': True,
                'message': message,
                'data': {
                    'id': application.id,
                    'registration_number': application.registration_number,
                    'status': application.status,
                    'action': action,
                }
            }, status=status.HTTP_201_CREATED)
            
        except ValidationError as e:
            return Response({
                'success': False,
                'message': _("Ariza yaratishda xatolik yuz berdi."),
                'errors': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'message': _("Kutilmagan xatolik yuz berdi."),
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

__all__ = [
    'ApplicationCreateAPIView'
]