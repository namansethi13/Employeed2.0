from django.db import models

class AddingStudentStatusType(models.TextChoices):
    NO_DATA = "NO_DATA", "No data"
    UPDATING = "UPDATING", "Updating"
    UPDATED = "UPDATED", "Updated"