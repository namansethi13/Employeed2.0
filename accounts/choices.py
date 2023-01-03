from django.db import models

class RoleType(models.TextChoices):
    COLLEGE = "COLLEGE", "College"
    STUDENT = "STUDENT", "Student"
    CORPORATE = "CORPORATE", "Corporate"
    OTHER = "OTHER", "Other"

class ShortRoleType(models.TextChoices):
    COLLEGE = "COLLEGE", "College"
    CORPORATE = "CORPORATE", "Corporate"