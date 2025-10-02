from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from apps.users.managers import CustomUserManager


class CustomUser(AbstractUser):
    phone_number = models.CharField(
        unique=True,    
        max_length=50,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,13}$",
                message="Phone number must be entered in the format: '+998991112233'. Up to 13 digits allowed.",
            )
        ],
        verbose_name=_("Phone number"),
    )
    password = models.CharField(max_length=128, verbose_name=_("Password"))
    username = models.CharField(max_length=30, verbose_name=_("Username"), unique=True)
    email = models.EmailField(verbose_name=_("Email"), unique=True)
    first_name = models.CharField(
        max_length=30, null=True, blank=True, verbose_name=_("First name")
    )
    last_name = models.CharField(
        max_length=30, null=True, blank=True, verbose_name=_("Last name")
    )
    avatar = models.ImageField(
        upload_to="avatars", null=True, blank=True, verbose_name=_("Avatar")
    )
    is_confirmed = models.BooleanField(default=False, verbose_name=_("Is Confirmed"))
    is_staff = models.BooleanField(default=False, verbose_name=_("Is Staff"))
    is_deleted = models.BooleanField(default=False, verbose_name=_("Is Deleted"))

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = [
        "username"
    ]  

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

        constraints = [
            models.UniqueConstraint(
                fields=["username"],
                condition=models.Q(is_deleted=False),
                name="unique_active_username",
            ),
        ]

    def delete_account(self):
        """Soft delete user account"""
        from django.utils import timezone

        timestamp = int(timezone.now().timestamp())

        self.phone_number = f"{self.phone_number}_deleted_{timestamp}"
        self.is_deleted = True
        self.save(update_fields=["phone_number", "is_deleted"])
