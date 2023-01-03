from django.db import models

class JobStatusType(models.TextChoices):
    PRIVATE = "PRIVATE", "Private"
    UPDATING = "UPDATING", "Updating"
    POSTED = "POSTED", "Posted"
    FINISHED = "FINISHED", "Finished"