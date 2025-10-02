import random
import string
from django.conf import settings
from django.db import IntegrityError
from django.core.mail import send_mail 


def generate_registration_number(length=20):
    """
    Kiritilgan uzunlikda (maks. 128) harflar va raqamlar aralashmasidan iborat
    registratsiya raqamini hosil qiladi.
    """
    characters = string.ascii_uppercase + string.digits
    
    if length > 128:
        length = 128
        
    reg_number = ''.join(random.choice(characters) for i in range(length))
    return reg_number


def send_application_email(application_instance):
    """
    Ariza muvaffaqiyatli yuborilganidan so'ng foydalanuvchiga elektron pochta xabarini yuboradi.
    """
    
    subject = f"Ariza qabul qilindi: {application_instance.registration_number}"
    message = (
        f"Hurmatli {application_instance.first_name} {application_instance.last_name},\n\n"
        f"Sizning arizangiz muvaffaqiyatli qabul qilindi.\n"
        f"Ro'yxatdan o'tish raqamingiz: {application_instance.registration_number}\n\n"
        f"Ariza holatini kuzatib boring."
    )
    recipient_list = [application_instance.email]
    print(recipient_list)
    
    try:
        send_mail(
            subject=subject, 
            message=message, 
            from_email="zarnigor1008@gmail.com",
            recipient_list=recipient_list,
            fail_silently=False,
        )
        print(f"DEBUG: Muvaffaqiyatli e-mail {application_instance.email} manziliga jo'natildi.")
    except Exception as e:
        print(f"CRITICAL ERROR: E-mail yuborishda xato yuz berdi: {e}")
