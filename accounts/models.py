import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from .choices import RoleType

class BaseUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    username = models.CharField(_("Username"), max_length=200, blank=True, null=True, editable=False)
    email = models.EmailField(_("email"), max_length=200, unique=True)
    role = models.CharField(max_length=9, choices=RoleType.choices, default=RoleType.OTHER)
    create_date = models.DateTimeField(auto_now_add=True)

    is_email_verified = models.BooleanField(_("Email Verified"), default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    # REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def __str__(self):
        return f"{self.username} {self.id}"

    def save(self, *args, **kwargs):
        self.username = str(self.email).split("@")[0]
        super(BaseUser, self).save(*args, **kwargs)


