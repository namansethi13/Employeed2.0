from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .choices import AddingStudentStatusType

BASEUSER = get_user_model()

class CollegeModel(BASEUSER):
    """
    College model 
    """

    address = models.CharField(_("Address"), max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.username}"

class CourseModel(models.Model):
    """
    Courses Model, it will have linked with College model as many to many relation
    """
    abbrevation = models.CharField(_('Course Appybbrevation'),max_length=10, unique=True)
    full_name = models.CharField(_('Full Name'), max_length=255)

    def __str__(self) -> str:
        return f"{self.abbrevation}"

    @classmethod
    def get_course_choice_options(cls):
        return [(course.abbrevation, course.abbrevation) for course in cls.objects.all()]


class CollegesCourses(models.Model):
    """
    Middle Model between College and Course, serve as a middle man for Many-to-Many 
    relation between College and Course Table
    """
    college = models.ForeignKey(related_name='courses',to=CollegeModel, on_delete=models.CASCADE)
    course = models.ForeignKey(related_name='colleges',to=CourseModel, on_delete=models.CASCADE)
    status = models.CharField(
        _("Adding Student Status"), 
        choices=AddingStudentStatusType.choices, 
        default=AddingStudentStatusType.NO_DATA,
        max_length=8
    )
    def __str__(self) -> str:
        return f"{self.college} | {self.course}"